# 🚀 PDF Outline Extractor

A high-performance containerized solution that extracts structured document outlines (Title + H1/H2/H3 headings) from PDF files in under 10 seconds.

## ✨ Quick Demo

```bash
# 1. Clone and enter directory
git clone <your-repo-url>
cd pdf-outline-extractor

# 2. Add your PDFs to input/
cp your-document.pdf input/

# 3. Run extractor
# Windows:
build.bat
# Linux/macOS:
./build.sh

# 4. Check results in output/
```

**Output Example:**
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Machine Learning", "page": 3 },
    { "level": "H3", "text": "Neural Networks", "page": 5 }
  ]
}
```

## 🏗️ Project Structure

```
├── src/
│   ├── main.py           # Main application
│   └── pdf_processor.py  # PDF processing logic
├── scripts/             # Development utilities
│   ├── run_local.py     # Local development runner
│   ├── test_processor.py # Testing utility
│   ├── validate.py      # Output validation
│   ├── demo.py          # Full demo workflow
│   └── README.md        # Scripts documentation
├── input/               # Place PDF files here
├── output/              # JSON results appear here
│   └── example_output.json  # Sample output format
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── build.bat           # Windows build script
├── build.sh            # Linux/macOS build script
└── README.md          # This file
```

## 🔧 Technical Details

- **Base Image**: python:3.10-slim
- **PDF Library**: PyMuPDF (fitz) for layout-aware parsing
- **Processing**: Rule-based heuristics using font analysis and pattern recognition
- **Performance**: Optimized for speed and accuracy
- **Size**: <200MB total footprint
- **Architecture**: AMD64 (x86_64) compatible

## 📋 Development & Testing

### Local Development
```bash
# Install dependencies
pip install PyMuPDF

# Run locally (without Docker)
python scripts/run_local.py
```

### Validation
Use the validation script to check output format compliance:

```bash
python scripts/validate.py
```

### Testing
```bash
# Add test PDFs to test_input/ directory
python scripts/test_processor.py
```

## 🎯 Hackathon Requirements

✅ **PDF Processing**: Extracts title and headings (H1/H2/H3)  
✅ **Performance**: <10 seconds per PDF, up to 50 pages  
✅ **Output**: Valid JSON format with heading level and page numbers  
✅ **Offline**: No web/API calls, fully containerized  
✅ **Architecture**: Compatible with AMD64 CPU architecture  
✅ **Model Size**: <200MB using lightweight rule-based approach
