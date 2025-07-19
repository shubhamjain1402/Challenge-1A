#!/bin/bash

# Build and test script for PDF Outline Extractor

echo "🚀 Building PDF Outline Extractor..."

# Create necessary directories
mkdir -p input output test_input test_output

# Build Docker image
echo "📦 Building Docker image..."
docker build --platform linux/amd64 -t pdf-outline-extractor:v1.0 .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    # Test if there are any PDF files in input directory
    if [ -f "input/*.pdf" ]; then
        echo "🔍 Testing with PDF files in input directory..."
        
        # Run the container
        docker run --rm \
            -v "$(pwd)/input:/app/input" \
            -v "$(pwd)/output:/app/output" \
            --network none \
            pdf-outline-extractor:v1.0
        
        echo "✅ Processing complete! Check output directory for results."
    else
        echo "ℹ️  No PDF files found in input directory."
        echo "   Add some PDF files to the 'input' directory and run:"
        echo "   docker run --rm -v \$(pwd)/input:/app/input -v \$(pwd)/output:/app/output --network none pdf-outline-extractor:v1.0"
    fi
else
    echo "❌ Docker build failed!"
    exit 1
fi
