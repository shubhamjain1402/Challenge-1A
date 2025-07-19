@echo off
REM Build and test script for PDF Outline Extractor (Windows)

echo 🚀 Building PDF Outline Extractor...

REM Create necessary directories
if not exist input mkdir input
if not exist output mkdir output
if not exist test_input mkdir test_input
if not exist test_output mkdir test_output

REM Build Docker image
echo 📦 Building Docker image...
docker build --platform linux/amd64 -t pdf-outline-extractor:v1.0 .

if %errorlevel% equ 0 (
    echo ✅ Docker image built successfully!
    
    REM Check if there are any PDF files in input directory
    if exist input\*.pdf (
        echo 🔍 Testing with PDF files in input directory...
        
        REM Run the container
        docker run --rm -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" --network none pdf-outline-extractor:v1.0
        
        echo ✅ Processing complete! Check output directory for results.
    ) else (
        echo ℹ️  No PDF files found in input directory.
        echo    Add some PDF files to the 'input' directory and run:
        echo    docker run --rm -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" --network none pdf-outline-extractor:v1.0
    )
) else (
    echo ❌ Docker build failed!
    exit /b 1
)
