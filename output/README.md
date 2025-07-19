# Output Directory

Processed JSON files will be saved here.

Each input PDF file will generate a corresponding JSON file with the same name.

## Output Format

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction",
      "page": 1
    },
    {
      "level": "H2",
      "text": "1.1 Overview",
      "page": 2
    },
    {
      "level": "H3",
      "text": "1.1.1 Background",
      "page": 3
    }
  ]
}
```

## File Naming

- Input: `document.pdf`
- Output: `document.json`

## Validation

Use the validation script to check output format:

```bash
python validate.py
```
