from src.pdf_processor import PDFProcessor
from pathlib import Path

processor = PDFProcessor()
files = ['file01.pdf', 'file02.pdf', 'file03.pdf']

for f in files:
    result = processor.extract_outline(Path(f'input/{f}'))
    print(f'{f}: {result}')
    print()
