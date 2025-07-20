from src.pdf_processor import PDFProcessor
from pathlib import Path
import json

processor = PDFProcessor()

# Test current vs expected outputs
files_to_check = ['file01.pdf', 'file02.pdf', 'file03.pdf', 'file04.pdf', 'file05.pdf']

for filename in files_to_check:
    print(f"\n=== {filename} ===")
    result = processor.extract_outline(Path(f'input/{filename}'))
    print(f"Current title: '{result['title']}'")
    print(f"Current outline count: {len(result['outline'])}")
    if result['outline']:
        print("Current outline preview:")
        for item in result['outline'][:3]:
            print(f"  {item['level']}: '{item['text']}' (page {item['page']})")
