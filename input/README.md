# Input Directory

Place your PDF files here for processing.

The Docker container will automatically detect and process all `.pdf` files in this directory.

## Example Usage

```bash
# Copy your PDF files to this directory
cp document1.pdf input/
cp document2.pdf input/

# Run the processor
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:v1.0
```

## Supported Files

- PDF files up to 50 pages
- Files with selectable text (not scanned images)
- Any PDF with structured headings and formatting
