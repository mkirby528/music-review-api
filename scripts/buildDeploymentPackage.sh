#!/bin/bash
echo "Installing dependencies..."
pip install  --target ./package -r src/requirements.txt
echo "Creating deployment package..."
cd package
zip -r ../archive.zip .
cd .. 
zip archive.zip -r src/
