# PDF Outline Extractor - Usage Examples

## Quick Start

1. **Build the Docker image:**
   ```bash
   # Linux/macOS
   ./build.sh
   
   # Windows
   build.bat
   ```

2. **Add PDF files to input directory:**
   ```bash
   mkdir input
   cp your-document.pdf input/
   ```

3. **Run the extractor:**
   ```bash
   docker run --rm \
     -v $(pwd)/input:/app/input \
     -v $(pwd)/output:/app/output \
     --network none \
     pdf-outline-extractor:v1.0
   ```

## Example Output

For a PDF titled "Understanding AI" with the following structure:

```
Understanding AI
├── 1. Introduction
├── 2. Machine Learning Basics
│   ├── 2.1 Supervised Learning
│   ├── 2.2 Unsupervised Learning
│   └── 2.3 Reinforcement Learning
├── 3. Deep Learning
│   ├── 3.1 Neural Networks
│   │   ├── 3.1.1 Perceptrons
│   │   └── 3.1.2 Multi-layer Networks
│   └── 3.2 Convolutional Networks
└── 4. Applications
```

The extractor will generate `understanding-ai.json`:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H1", "text": "Machine Learning Basics", "page": 2 },
    { "level": "H2", "text": "Supervised Learning", "page": 3 },
    { "level": "H2", "text": "Unsupervised Learning", "page": 5 },
    { "level": "H2", "text": "Reinforcement Learning", "page": 7 },
    { "level": "H1", "text": "Deep Learning", "page": 10 },
    { "level": "H2", "text": "Neural Networks", "page": 11 },
    { "level": "H3", "text": "Perceptrons", "page": 12 },
    { "level": "H3", "text": "Multi-layer Networks", "page": 14 },
    { "level": "H2", "text": "Convolutional Networks", "page": 18 },
    { "level": "H1", "text": "Applications", "page": 25 }
  ]
}
```

## Heading Detection Rules

The extractor uses multiple heuristics to identify headings:

### 1. Font Size Analysis
- **H1**: Large fonts (typically 14pt+), often document titles or main sections
- **H2**: Medium fonts (typically 12pt+), subsections
- **H3**: Smaller fonts (typically 10pt+), sub-subsections

### 2. Pattern Recognition
- Numbered sections: "1. Introduction", "2.1 Overview", "2.1.1 Details"
- Roman numerals: "I. Introduction", "II. Methods"
- Letter sections: "A. Overview", "B. Details"
- Keywords: "Chapter 1", "Section 2"

### 3. Formatting Cues
- **Bold text** with appropriate font size
- **ALL CAPS** headers
- **Title Case** formatting
- Position on page (headings often appear at top of sections)

### 4. Contextual Analysis
- Text length (headings are typically shorter)
- Line spacing (headings often have more space around them)
- Consistent formatting patterns within document

## Performance Specifications

- **Processing Speed**: < 10 seconds per PDF
- **Page Limit**: Up to 50 pages per document
- **Model Size**: < 200MB (uses lightweight rule-based approach)
- **Memory Usage**: Low memory footprint with streaming processing
- **Offline Operation**: No internet connection required

## Troubleshooting

### Common Issues

1. **No headings detected**
   - Check if PDF has selectable text (not scanned images)
   - Verify headings have distinct formatting (font size, bold, etc.)

2. **Missing headings**
   - Some PDFs use non-standard formatting
   - Complex layouts may require manual adjustment

3. **Incorrect heading levels**
   - The extractor makes best-effort classification
   - Review output and adjust post-processing if needed

### Testing

Use the included test script to validate extraction:

```bash
python test_processor.py
```

Add test PDFs to `test_input/` directory and run the script to see detailed analysis.

## Architecture

```
┌─────────────────┐
│   PDF Input     │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  PyMuPDF        │
│  Document       │
│  Parser         │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Font Analysis  │
│  & Pattern      │
│  Recognition    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Heading        │
│  Classification │
│  & Filtering    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  JSON Output    │
└─────────────────┘
```

## Technical Details

- **Base Image**: `python:3.10-slim` (lightweight, secure)
- **PDF Library**: PyMuPDF (fitz) - fast, reliable PDF parsing
- **Text Processing**: Rule-based heuristics with regex patterns
- **Output Format**: Clean JSON with UTF-8 encoding
- **Error Handling**: Graceful degradation with error logging
