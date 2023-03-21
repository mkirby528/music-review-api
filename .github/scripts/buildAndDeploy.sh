#!/bin/bash

echo "Installing dependencies..."
pip install  --target ./package -r src/requirements.txt
echo "Creating deployment package..."
cd package
zip -r ../archive.zip .
cd .. 
zip archive.zip -r src/

echo "Uploading code to ${LAMBDA_NAME} in ${AWS_REGION} "
aws lambda update-function-code \
--function-name ${LAMBDA_NAME} \
--region ${AWS_REGION} \
--zip-file fileb://archive.zip
