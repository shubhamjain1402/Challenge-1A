# 🚀 Quick Start Guide

## For Users Who Want to Test This Project

### **Prerequisites**
- Docker Desktop installed and running
- PDF files with text content (not scanned images)

### **Step 1: Get the Project**
```bash
git clone <your-repo-url>
cd pdf-outline-extractor
```

### **Step 2: Add Your PDF Files**
```bash
# Copy your PDF files to the input directory
cp your-document.pdf input/
```

### **Step 3: Run the Extractor**

#### **Windows:**
```cmd
build.bat
```

#### **Linux/macOS:**
```bash
chmod +x build.sh
./build.sh
```

#### **Manual Docker Commands:**
```bash
# Build the image
docker build --platform linux/amd64 -t pdf-outline-extractor:v1.0 .

# Run the container
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:v1.0
```

### **Step 4: Check Results**
- JSON files will appear in the `output/` directory
- Each PDF generates a corresponding JSON file
- See `output/example_output.json` for format reference

### **Example Output**
```json
{
  "title": "Your Document Title",
  "outline": [
    { "level": "H1", "text": "Chapter 1", "page": 1 },
    { "level": "H2", "text": "Section 1.1", "page": 2 },
    { "level": "H3", "text": "Subsection 1.1.1", "page": 3 }
  ]
}
```

## **🛠️ For Developers**

### **Local Development**
```bash
# Install dependencies
pip install PyMuPDF

# Run without Docker
python scripts/run_local.py
```

### **Testing**
```bash
# Validate outputs
python scripts/validate.py

# Run tests
python scripts/test_processor.py
```

### **Project Structure**
```
├── src/              # Core application
├── scripts/          # Development tools
├── input/           # Put PDF files here
├── output/          # JSON results appear here
├── Dockerfile       # Container setup
└── build.bat/sh     # Build scripts
```

## **🎯 What This Does**

- ✅ Extracts document title and headings (H1/H2/H3) from PDFs
- ✅ Processes files in under 10 seconds
- ✅ Works offline (no internet required)
- ✅ Handles up to 50 pages per PDF
- ✅ Outputs clean JSON format with page numbers
- ✅ Uses rule-based detection (font size, formatting, patterns)

## **⚡ Troubleshooting**

**Docker not working?**
- Make sure Docker Desktop is running
- Try: `docker --version` to verify installation

**No headings detected?**
- Ensure PDF has selectable text (not scanned images)
- Check that headings have distinct formatting (bold, larger fonts)

**Permission errors?**
- Make sure Docker has access to your project directory
- Try running as administrator if needed
