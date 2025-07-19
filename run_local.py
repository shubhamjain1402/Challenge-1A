#!/usr/bin/env python3
"""
Local PDF Outline Extractor - Main Application
Extracts structured document outlines from PDF files in local directories.
"""

import os
import json
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pdf_processor import PDFProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

def main():
    """Main application entry point."""
    logger.info("Starting PDF Outline Extractor (Local Version)")
    
    # Ensure directories exist
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all PDF files in input directory
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {INPUT_DIR} directory")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF file(s) to process")
    
    # Initialize PDF processor
    processor = PDFProcessor()
    
    # Process each PDF file
    for pdf_file in pdf_files:
        try:
            logger.info(f"Processing: {pdf_file.name}")
            
            # Extract outline
            result = processor.extract_outline(pdf_file)
            
            # Generate output filename
            output_file = OUTPUT_DIR / f"{pdf_file.stem}.json"
            
            # Write JSON output
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully processed {pdf_file.name} -> {output_file.name}")
            
            # Print summary
            print(f"\n{'='*60}")
            print(f"📄 PROCESSED: {pdf_file.name}")
            print(f"{'='*60}")
            print(f"📖 Title: {result['title']}")
            print(f"📋 Headings found: {len(result['outline'])}")
            print(f"💾 Output saved to: {output_file}")
            
            if result['outline']:
                print(f"\n📑 Outline Preview:")
                for i, heading in enumerate(result['outline'][:10], 1):
                    indent = "  " * (int(heading['level'][1]) - 1)
                    print(f"{i:2d}. {indent}{heading['level']}: {heading['text']} (page {heading['page']})")
                
                if len(result['outline']) > 10:
                    print(f"    ... and {len(result['outline']) - 10} more headings")
            
            print(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"Error processing {pdf_file.name}: {str(e)}")
            
            # Create error output
            error_result = {
                "title": "Error",
                "outline": [],
                "error": str(e)
            }
            
            output_file = OUTPUT_DIR / f"{pdf_file.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(error_result, f, indent=2, ensure_ascii=False)
    
    logger.info("PDF processing complete")

if __name__ == "__main__":
    main()
