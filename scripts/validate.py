#!/usr/bin/env python3
"""
Validation script for PDF Outline Extractor
Tests the solution against requirements and validates output format.
"""

import json
import time
import logging
import os
from pathlib import Path
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolutionValidator:
    """Validates the PDF outline extractor solution against requirements."""
    
    def __init__(self):
        self.requirements = {
            "max_processing_time": 10.0,  # seconds per PDF
            "max_pages": 50,
            "required_output_fields": ["title", "outline"],
            "required_heading_fields": ["level", "text", "page"],
            "valid_heading_levels": ["H1", "H2", "H3"]
        }
    
    def validate_output_format(self, output_file: Path) -> Dict[str, Any]:
        """
        Validate the JSON output format against requirements.
        
        Args:
            output_file: Path to output JSON file
            
        Returns:
            Validation results dictionary
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "stats": {}
        }
        
        try:
            # Load and parse JSON
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check required top-level fields
            for field in self.requirements["required_output_fields"]:
                if field not in data:
                    results["errors"].append(f"Missing required field: {field}")
                    results["valid"] = False
            
            # Validate title
            if "title" in data:
                if not isinstance(data["title"], str):
                    results["errors"].append("Title must be a string")
                    results["valid"] = False
                elif len(data["title"]) == 0:
                    results["warnings"].append("Title is empty")
            
            # Validate outline
            if "outline" in data:
                if not isinstance(data["outline"], list):
                    results["errors"].append("Outline must be a list")
                    results["valid"] = False
                else:
                    # Validate each heading
                    for i, heading in enumerate(data["outline"]):
                        heading_errors = self._validate_heading(heading, i)
                        results["errors"].extend(heading_errors)
                        if heading_errors:
                            results["valid"] = False
                    
                    # Collect statistics
                    results["stats"] = self._collect_outline_stats(data["outline"])
            
        except json.JSONDecodeError as e:
            results["errors"].append(f"Invalid JSON format: {str(e)}")
            results["valid"] = False
        except Exception as e:
            results["errors"].append(f"Error reading file: {str(e)}")
            results["valid"] = False
        
        return results
    
    def _validate_heading(self, heading: Dict[str, Any], index: int) -> List[str]:
        """Validate a single heading object."""
        errors = []
        
        # Check required fields
        for field in self.requirements["required_heading_fields"]:
            if field not in heading:
                errors.append(f"Heading {index}: Missing required field '{field}'")
        
        # Validate level
        if "level" in heading:
            if heading["level"] not in self.requirements["valid_heading_levels"]:
                errors.append(f"Heading {index}: Invalid level '{heading['level']}'")
        
        # Validate text
        if "text" in heading:
            if not isinstance(heading["text"], str):
                errors.append(f"Heading {index}: Text must be a string")
            elif len(heading["text"]) == 0:
                errors.append(f"Heading {index}: Text cannot be empty")
        
        # Validate page
        if "page" in heading:
            if not isinstance(heading["page"], int):
                errors.append(f"Heading {index}: Page must be an integer")
            elif heading["page"] < 1:
                errors.append(f"Heading {index}: Page must be positive")
            elif heading["page"] > self.requirements["max_pages"]:
                errors.append(f"Heading {index}: Page {heading['page']} exceeds max pages ({self.requirements['max_pages']})")
        
        return errors
    
    def _collect_outline_stats(self, outline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Collect statistics about the outline."""
        stats = {
            "total_headings": len(outline),
            "levels": {"H1": 0, "H2": 0, "H3": 0},
            "pages_with_headings": set(),
            "max_page": 0
        }
        
        for heading in outline:
            if "level" in heading and heading["level"] in stats["levels"]:
                stats["levels"][heading["level"]] += 1
            
            if "page" in heading:
                stats["pages_with_headings"].add(heading["page"])
                stats["max_page"] = max(stats["max_page"], heading["page"])
        
        stats["pages_with_headings"] = len(stats["pages_with_headings"])
        return stats
    
    def validate_solution(self, input_dir: Path, output_dir: Path) -> Dict[str, Any]:
        """
        Validate the complete solution against all requirements.
        
        Args:
            input_dir: Directory containing input PDF files
            output_dir: Directory containing output JSON files
            
        Returns:
            Overall validation results
        """
        results = {
            "valid": True,
            "total_files": 0,
            "processed_files": 0,
            "failed_files": 0,
            "validation_errors": [],
            "file_results": {},
            "performance": {}
        }
        
        # Find all PDF files
        pdf_files = list(input_dir.glob("*.pdf"))
        results["total_files"] = len(pdf_files)
        
        if not pdf_files:
            results["validation_errors"].append("No PDF files found in input directory")
            results["valid"] = False
            return results
        
        # Check each PDF has corresponding output
        for pdf_file in pdf_files:
            output_file = output_dir / f"{pdf_file.stem}.json"
            
            if not output_file.exists():
                results["failed_files"] += 1
                results["validation_errors"].append(f"Missing output file for {pdf_file.name}")
                results["valid"] = False
                continue
            
            # Validate output format
            file_results = self.validate_output_format(output_file)
            results["file_results"][pdf_file.name] = file_results
            
            if file_results["valid"]:
                results["processed_files"] += 1
            else:
                results["failed_files"] += 1
                results["valid"] = False
        
        # Calculate success rate
        if results["total_files"] > 0:
            success_rate = results["processed_files"] / results["total_files"]
            results["performance"]["success_rate"] = success_rate
        
        return results
    
    def print_validation_report(self, results: Dict[str, Any]):
        """Print a formatted validation report."""
        print("\n" + "="*60)
        print("📋 PDF OUTLINE EXTRACTOR VALIDATION REPORT")
        print("="*60)
        
        # Overall status
        status = "✅ PASSED" if results["valid"] else "❌ FAILED"
        print(f"Overall Status: {status}")
        print(f"Files Processed: {results['processed_files']}/{results['total_files']}")
        
        if results["total_files"] > 0:
            success_rate = results["processed_files"] / results["total_files"] * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        # Global errors
        if results["validation_errors"]:
            print(f"\n🚨 Global Issues ({len(results['validation_errors'])}):")
            for error in results["validation_errors"]:
                print(f"  • {error}")
        
        # File-specific results
        if results["file_results"]:
            print(f"\n📄 File-by-File Results:")
            for filename, file_result in results["file_results"].items():
                status = "✅" if file_result["valid"] else "❌"
                print(f"  {status} {filename}")
                
                if file_result["stats"]:
                    stats = file_result["stats"]
                    print(f"    └─ {stats['total_headings']} headings, {stats['pages_with_headings']} pages")
                    print(f"       H1: {stats['levels']['H1']}, H2: {stats['levels']['H2']}, H3: {stats['levels']['H3']}")
                
                if file_result["errors"]:
                    print(f"    └─ Errors: {len(file_result['errors'])}")
                    for error in file_result["errors"][:3]:  # Show first 3 errors
                        print(f"       • {error}")
                    if len(file_result["errors"]) > 3:
                        print(f"       • ... and {len(file_result['errors']) - 3} more")
                
                if file_result["warnings"]:
                    print(f"    └─ Warnings: {len(file_result['warnings'])}")
                    for warning in file_result["warnings"][:2]:
                        print(f"       • {warning}")
        
        print("\n" + "="*60)

def main():
    """Main validation function."""
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    validator = SolutionValidator()
    
    # Default paths (relative to project root)
    input_dir = Path("input")
    output_dir = Path("output")
    
    # Check if directories exist
    if not input_dir.exists():
        print(f"❌ Input directory '{input_dir}' does not exist")
        return
    
    if not output_dir.exists():
        print(f"❌ Output directory '{output_dir}' does not exist")
        return
    
    # Run validation
    print("🔍 Starting validation...")
    results = validator.validate_solution(input_dir, output_dir)
    
    # Print report
    validator.print_validation_report(results)
    
    # Exit with appropriate code
    if results["valid"]:
        print("✅ Validation completed successfully!")
        exit(0)
    else:
        print("❌ Validation failed!")
        exit(1)

if __name__ == "__main__":
    main()
