#!/usr/bin/env python3
"""
PDF Processor - Core PDF parsing and outline extraction logic
Uses PyMuPDF for layout-aware PDF processing with rule-based heuristics.
"""

import fitz  # PyMuPDF
import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF parsing and outline extraction using rule-based heuristics."""
    
    def __init__(self):
        """Initialize the PDF processor with default settings."""
        self.max_pages = 50
        
        # Font size thresholds for heading detection
        self.title_min_size = 16
        self.h1_min_size = 14
        self.h2_min_size = 12
        self.h3_min_size = 10
        
        # Common heading patterns
        self.heading_patterns = [
            r'^\d+\.\s+',  # "1. Introduction"
            r'^\d+\.\d+\s+',  # "1.1 Overview"
            r'^\d+\.\d+\.\d+\s+',  # "1.1.1 Details"
            r'^[A-Z][A-Z\s]+$',  # "INTRODUCTION"
            r'^Chapter\s+\d+',  # "Chapter 1"
            r'^Section\s+\d+',  # "Section 1"
            r'^[IVX]+\.\s+',  # "I. Introduction"
            r'^[A-Z]\.\s+',  # "A. Overview"
        ]
        
        # Compile regex patterns
        self.compiled_patterns = [re.compile(pattern) for pattern in self.heading_patterns]
    
    def extract_outline(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extract structured outline from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary containing title and outline structure
        """
        try:
            # Open PDF document
            doc = fitz.open(pdf_path)
            
            # Limit pages to max_pages
            total_pages = min(len(doc), self.max_pages)
            
            # Extract title
            title = self._extract_title(doc)
            
            # Extract outline
            outline = self._extract_headings(doc, total_pages)
            
            doc.close()
            
            return {
                "title": title,
                "outline": outline
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise
    
    def _extract_title(self, doc: fitz.Document) -> str:
        """
        Extract document title from PDF metadata or first page.
        
        Args:
            doc: PyMuPDF document object
            
        Returns:
            Document title string
        """
        # Try to get title from metadata
        metadata = doc.metadata
        if metadata.get('title'):
            title = metadata['title'].strip()
            if title and len(title) > 0:
                return title
        
        # Try to extract title from first page
        if len(doc) > 0:
            first_page = doc[0]
            title = self._extract_title_from_page(first_page)
            if title:
                return title
        
        return "Untitled Document"
    
    def _extract_title_from_page(self, page: fitz.Page) -> Optional[str]:
        """
        Extract title from the first page using font analysis.
        
        Args:
            page: PyMuPDF page object
            
        Returns:
            Title string or None
        """
        try:
            # Get text blocks with font information
            blocks = page.get_text("dict")
            
            # Find largest font size text in upper portion of page
            candidates = []
            page_height = page.rect.height
            
            for block in blocks.get("blocks", []):
                if "lines" not in block:
                    continue
                
                for line in block["lines"]:
                    # Only consider text in upper 30% of page for title
                    if line.get("bbox", [0, 0, 0, 0])[1] > page_height * 0.3:
                        continue
                    
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        font_size = span.get("size", 0)
                        
                        if text and font_size >= self.title_min_size:
                            candidates.append({
                                "text": text,
                                "size": font_size,
                                "y": line.get("bbox", [0, 0, 0, 0])[1]
                            })
            
            # Sort by font size (descending) and position (ascending)
            candidates.sort(key=lambda x: (-x["size"], x["y"]))
            
            if candidates:
                # Return the largest, highest text as title
                title = candidates[0]["text"]
                # Clean up title
                title = re.sub(r'\s+', ' ', title).strip()
                return title
            
        except Exception as e:
            logger.warning(f"Error extracting title from page: {str(e)}")
        
        return None
    
    def _extract_headings(self, doc: fitz.Document, total_pages: int) -> List[Dict[str, Any]]:
        """
        Extract headings from PDF using rule-based heuristics.
        
        Args:
            doc: PyMuPDF document object
            total_pages: Number of pages to process
            
        Returns:
            List of heading dictionaries
        """
        headings = []
        
        for page_num in range(total_pages):
            try:
                page = doc[page_num]
                page_headings = self._extract_headings_from_page(page, page_num + 1)
                headings.extend(page_headings)
            except Exception as e:
                logger.warning(f"Error processing page {page_num + 1}: {str(e)}")
                continue
        
        return self._post_process_headings(headings)
    
    def _extract_headings_from_page(self, page: fitz.Page, page_num: int) -> List[Dict[str, Any]]:
        """
        Extract headings from a single page.
        
        Args:
            page: PyMuPDF page object
            page_num: Page number (1-based)
            
        Returns:
            List of heading dictionaries
        """
        headings = []
        
        try:
            # Get text blocks with font information
            blocks = page.get_text("dict")
            
            # Analyze font sizes across the page
            font_sizes = []
            for block in blocks.get("blocks", []):
                if "lines" not in block:
                    continue
                
                for line in block["lines"]:
                    for span in line.get("spans", []):
                        font_size = span.get("size", 0)
                        if font_size > 0:
                            font_sizes.append(font_size)
            
            # Calculate font size thresholds dynamically
            if font_sizes:
                font_sizes.sort(reverse=True)
                avg_size = sum(font_sizes) / len(font_sizes)
                
                # Adaptive thresholds based on document
                dynamic_h1 = max(self.h1_min_size, avg_size * 1.3)
                dynamic_h2 = max(self.h2_min_size, avg_size * 1.15)
                dynamic_h3 = max(self.h3_min_size, avg_size * 1.05)
            else:
                dynamic_h1 = self.h1_min_size
                dynamic_h2 = self.h2_min_size
                dynamic_h3 = self.h3_min_size
            
            # Extract potential headings
            for block in blocks.get("blocks", []):
                if "lines" not in block:
                    continue
                
                for line in block["lines"]:
                    line_text = ""
                    max_font_size = 0
                    is_bold = False
                    
                    # Combine spans in line
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        font_size = span.get("size", 0)
                        font_flags = span.get("flags", 0)
                        
                        if text:
                            line_text += text + " "
                            max_font_size = max(max_font_size, font_size)
                            
                            # Check if text is bold (font flags & 16)
                            if font_flags & 16:
                                is_bold = True
                    
                    line_text = line_text.strip()
                    
                    # Skip empty lines or very long lines (likely paragraphs)
                    if not line_text or len(line_text) > 200:
                        continue
                    
                    # Determine heading level
                    heading_level = self._determine_heading_level(
                        line_text, max_font_size, is_bold, 
                        dynamic_h1, dynamic_h2, dynamic_h3
                    )
                    
                    if heading_level:
                        headings.append({
                            "level": heading_level,
                            "text": self._clean_heading_text(line_text),
                            "page": page_num,
                            "font_size": max_font_size,
                            "is_bold": is_bold
                        })
        
        except Exception as e:
            logger.warning(f"Error extracting headings from page {page_num}: {str(e)}")
        
        return headings
    
    def _determine_heading_level(self, text: str, font_size: float, is_bold: bool, 
                                h1_threshold: float, h2_threshold: float, h3_threshold: float) -> Optional[str]:
        """
        Determine if text is a heading and classify its level.
        
        Args:
            text: Text content
            font_size: Font size
            is_bold: Whether text is bold
            h1_threshold: H1 font size threshold
            h2_threshold: H2 font size threshold
            h3_threshold: H3 font size threshold
            
        Returns:
            Heading level string or None
        """
        # Check for pattern-based headings
        pattern_level = self._check_heading_patterns(text)
        
        # Font-based classification
        font_level = None
        if font_size >= h1_threshold:
            font_level = "H1"
        elif font_size >= h2_threshold:
            font_level = "H2"
        elif font_size >= h3_threshold:
            font_level = "H3"
        
        # Combine pattern and font analysis
        if pattern_level:
            return pattern_level
        
        # If text is bold and has reasonable font size, consider it a heading
        if is_bold and font_level:
            return font_level
        
        # Additional heuristics
        if font_level == "H1" and (is_bold or self._looks_like_heading(text)):
            return "H1"
        elif font_level == "H2" and (is_bold or self._looks_like_heading(text)):
            return "H2"
        elif font_level == "H3" and (is_bold or self._looks_like_heading(text)):
            return "H3"
        
        return None
    
    def _check_heading_patterns(self, text: str) -> Optional[str]:
        """
        Check if text matches common heading patterns.
        
        Args:
            text: Text to check
            
        Returns:
            Heading level or None
        """
        for pattern in self.compiled_patterns:
            if pattern.match(text):
                # Determine level based on pattern
                if re.match(r'^\d+\.\d+\.\d+\s+', text):
                    return "H3"
                elif re.match(r'^\d+\.\d+\s+', text):
                    return "H2"
                elif re.match(r'^\d+\.\s+', text):
                    return "H1"
                else:
                    return "H1"  # Default for other patterns
        
        return None
    
    def _looks_like_heading(self, text: str) -> bool:
        """
        Check if text looks like a heading using additional heuristics.
        
        Args:
            text: Text to check
            
        Returns:
            True if text looks like a heading
        """
        # Short text (likely heading)
        if len(text) < 100:
            # Starts with capital letter
            if text[0].isupper():
                # Contains multiple capital letters or is title case
                if sum(1 for c in text if c.isupper()) >= 2:
                    return True
                # Check for title case
                words = text.split()
                if len(words) >= 2 and all(word[0].isupper() for word in words if word):
                    return True
        
        return False
    
    def _clean_heading_text(self, text: str) -> str:
        """
        Clean and normalize heading text.
        
        Args:
            text: Raw heading text
            
        Returns:
            Cleaned heading text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove common artifacts
        text = re.sub(r'^[•\-\*\+]\s*', '', text)  # Remove bullet points
        text = re.sub(r'^\s*[\.]+\s*', '', text)  # Remove leading dots
        
        return text
    
    def _post_process_headings(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Post-process headings to remove duplicates and improve structure.
        
        Args:
            headings: List of raw headings
            
        Returns:
            Processed headings list
        """
        if not headings:
            return []
        
        # Remove duplicates (same text on same page)
        seen = set()
        unique_headings = []
        
        for heading in headings:
            key = (heading["text"], heading["page"])
            if key not in seen:
                seen.add(key)
                unique_headings.append(heading)
        
        # Sort by page and font size (descending)
        unique_headings.sort(key=lambda x: (x["page"], -x.get("font_size", 0)))
        
        # Clean up the output format
        result = []
        for heading in unique_headings:
            result.append({
                "level": heading["level"],
                "text": heading["text"],
                "page": heading["page"]
            })
        
        return result
