# Development Scripts

This directory contains development and testing utilities for the PDF Outline Extractor.

## 🛠️ Available Scripts

### **`run_local.py`**
Local development runner that processes PDFs without Docker.

```bash
# Install dependencies first
pip install PyMuPDF

# Run locally
python scripts/run_local.py
```

### **`test_processor.py`** 
Test script for development and debugging.

```bash
# Add test PDFs to test_input/ directory
python scripts/test_processor.py
```

### **`validate.py`**
Validates output JSON format against requirements.

```bash
# After processing PDFs, validate outputs
python scripts/validate.py
```

### **`demo.py`**
Complete demo workflow showing build and test process.

```bash
# Full demonstration
python scripts/demo.py
```

## 📁 Directory Structure

```
scripts/
├── README.md           # This file
├── run_local.py        # Local development runner
├── test_processor.py   # Testing utility
├── validate.py         # Output validation
└── demo.py             # Full demo workflow
```

## 🚀 For Production Use

Use the main Docker workflow instead:

```bash
# Build and run with Docker
build.bat

# Or manually
docker build --platform linux/amd64 -t pdf-outline-extractor:v1.0 .
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none pdf-outline-extractor:v1.0
```
