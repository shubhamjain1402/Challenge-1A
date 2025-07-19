#!/usr/bin/env python3
"""
Complete solution demonstration script
Shows the entire workflow from build to validation
"""

import subprocess
import sys
import time
import json
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle output."""
    print(f"🔧 {description}")
    print(f"   Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Success")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"   ❌ Failed")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False

def main():
    """Demonstrate the complete solution."""
    
    print("🚀 PDF Outline Extractor - Complete Solution Demo")
    print("=" * 60)
    
    # Check if Docker is available
    if not run_command("docker --version", "Checking Docker availability"):
        print("❌ Docker is not available. Please install Docker to run this demo.")
        return
    
    # Build the Docker image
    print("\n📦 Building Docker Image...")
    build_cmd = "docker build --platform linux/amd64 -t pdf-outline-extractor:v1.0 ."
    
    if not run_command(build_cmd, "Building Docker image"):
        print("❌ Failed to build Docker image")
        return
    
    # Check for input files
    input_dir = Path("input")
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if pdf_files:
        print(f"\n📄 Found {len(pdf_files)} PDF file(s) to process:")
        for pdf in pdf_files:
            print(f"   • {pdf.name}")
        
        # Run the processor
        print("\n🏃 Running PDF Processor...")
        run_cmd = f"docker run --rm -v {Path.cwd()}/input:/app/input -v {Path.cwd()}/output:/app/output --network none pdf-outline-extractor:v1.0"
        
        if run_command(run_cmd, "Processing PDF files"):
            print("✅ PDF processing completed successfully!")
            
            # Check output files
            output_dir = Path("output")
            json_files = list(output_dir.glob("*.json"))
            
            print(f"\n📋 Generated {len(json_files)} output file(s):")
            for json_file in json_files:
                print(f"   • {json_file.name}")
                
                # Show sample content
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    print(f"     Title: {data.get('title', 'N/A')}")
                    print(f"     Headings: {len(data.get('outline', []))}")
                    
                    # Show first few headings
                    outline = data.get('outline', [])
                    for i, heading in enumerate(outline[:3]):
                        print(f"     {heading.get('level', 'N/A')}: {heading.get('text', 'N/A')} (page {heading.get('page', 'N/A')})")
                    
                    if len(outline) > 3:
                        print(f"     ... and {len(outline) - 3} more headings")
                
                except Exception as e:
                    print(f"     ❌ Error reading output: {str(e)}")
                
                print()
            
            # Run validation
            print("🔍 Running output validation...")
            if run_command("python validate.py", "Validating output format"):
                print("✅ All outputs are valid!")
            else:
                print("⚠️  Some validation issues found - check the report above")
        
        else:
            print("❌ PDF processing failed")
    
    else:
        print("\n📄 No PDF files found in input directory")
        print("   To test the solution:")
        print("   1. Add some PDF files to the 'input' directory")
        print("   2. Run this script again")
        print("   3. Or use the Docker command directly:")
        print("      docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:v1.0")
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed!")
    print("\nNext steps:")
    print("• Add PDF files to 'input' directory")
    print("• Run: docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:v1.0")
    print("• Check 'output' directory for results")
    print("• Use validate.py to verify output format")

if __name__ == "__main__":
    main()
