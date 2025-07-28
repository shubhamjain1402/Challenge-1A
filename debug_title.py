import fitz
from src.pdf_processor import PDFProcessor

doc = fitz.open('input/file01.pdf')
processor = PDFProcessor()

# Check metadata
print('PDF Metadata:')
print(doc.metadata)
print()

# Check first page text extraction
page = doc[0]
print('Page text analysis:')
blocks = page.get_text('dict')
for block in blocks.get('blocks', []):
    if 'lines' not in block:
        continue
    for line in block['lines']:
        y_pos = line.get('bbox', [0, 0, 0, 0])[1] 
        page_height = page.rect.height
        for span in line.get('spans', []):
            text = span.get('text', '').strip()
            size = span.get('size', 0)
            if text and len(text) > 5:
                print(f'Y: {y_pos}/{page_height} ({y_pos/page_height*100:.1f}%) | Size: {size} | Text: "{text}"')

# Test the looks_like_filename method
title_from_metadata = doc.metadata.get('title', '')
print(f'\nMetadata title: "{title_from_metadata}"')
print(f'Looks like filename: {processor._looks_like_filename(title_from_metadata)}')

# Test content title extraction
content_title = processor._extract_title_from_page(page)
print(f'Content title: "{content_title}"')

doc.close()
