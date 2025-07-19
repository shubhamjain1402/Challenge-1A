#!/usr/bin/env python3
"""
Test script for PDF Outline Extractor
"""

import sys
import json
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pdf_processor import PDFProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_pdf_processor():
    """Test the PDF processor with sample files."""
    
    # Create test directories
    test_input = Path("test_input")
    test_output = Path("test_output")
    
    test_input.mkdir(exist_ok=True)
    test_output.mkdir(exist_ok=True)
    
    logger.info("Test directories created")
    
    # Initialize processor
    processor = PDFProcessor()
    
    # Look for test PDF files
    pdf_files = list(test_input.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning("No PDF files found in test_input directory")
        logger.info("Please add some PDF files to test_input/ directory to test")
        return
    
    for pdf_file in pdf_files:
        try:
            logger.info(f"Testing with: {pdf_file.name}")
            
            # Extract outline
            result = processor.extract_outline(pdf_file)
            
            # Save result
            output_file = test_output / f"{pdf_file.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Result saved to: {output_file}")
            
            # Print summary
            print(f"\n--- {pdf_file.name} ---")
            print(f"Title: {result['title']}")
            print(f"Headings found: {len(result['outline'])}")
            
            for heading in result['outline'][:5]:  # Show first 5 headings
                print(f"  {heading['level']}: {heading['text']} (page {heading['page']})")
            
            if len(result['outline']) > 5:
                print(f"  ... and {len(result['outline']) - 5} more")
            
        except Exception as e:
            logger.error(f"Error testing {pdf_file.name}: {str(e)}")

if __name__ == "__main__":
    test_pdf_processor()
