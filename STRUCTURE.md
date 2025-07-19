# Project Structure

```
adobe-github/
├── README.md                 # Main project documentation
├── EXAMPLES.md              # Usage examples and technical details
├── Dockerfile               # Docker container configuration
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── .dockerignore           # Docker ignore rules
├── build.sh                # Linux/macOS build script
├── build.bat               # Windows build script
├── test_processor.py       # Local testing script
├── validate.py             # Output validation script
├── src/
│   ├── main.py             # Main application entry point
│   └── pdf_processor.py    # Core PDF processing logic
├── input/                  # Input PDF files (created at runtime)
├── output/                 # Output JSON files (created at runtime)
├── test_input/             # Test PDF files (for local testing)
└── test_output/            # Test JSON outputs (for local testing)
```

## Quick Start Commands

### Build and Run
```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-outline-extractor:v1.0 .

# Run with your PDF files
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:v1.0
```

### Development and Testing
```bash
# Run local tests (requires Python 3.10+)
python test_processor.py

# Validate output format
python validate.py
```

## Core Components

### 1. PDF Processor (`src/pdf_processor.py`)
- **Title Extraction**: From metadata or first page analysis
- **Heading Detection**: Multi-layered heuristics using:
  - Font size analysis with adaptive thresholds
  - Pattern recognition (numbered sections, etc.)
  - Formatting cues (bold, caps, positioning)
  - Contextual analysis (length, spacing)

### 2. Main Application (`src/main.py`)
- **File Discovery**: Auto-detects PDFs in `/app/input`
- **Batch Processing**: Processes multiple PDFs efficiently
- **Error Handling**: Graceful failure with error logging
- **JSON Output**: Structured output in `/app/output`

### 3. Docker Configuration (`Dockerfile`)
- **Base Image**: `python:3.10-slim` for minimal footprint
- **Dependencies**: PyMuPDF for PDF parsing
- **Offline Operation**: No network access required
- **Volume Mounting**: Input/output directory mapping

## Key Features

✅ **Performance**: < 10 seconds per PDF
✅ **Scalability**: Handles up to 50 pages per document
✅ **Accuracy**: Multi-heuristic heading detection
✅ **Reliability**: Comprehensive error handling
✅ **Compliance**: Fully offline, no API calls
✅ **Compatibility**: AMD64 architecture support
✅ **Lightweight**: < 200MB total size

## Testing Strategy

1. **Unit Testing**: Individual component validation
2. **Integration Testing**: End-to-end workflow testing
3. **Format Validation**: JSON schema compliance
4. **Performance Testing**: Speed and memory usage
5. **Error Testing**: Graceful failure scenarios
