#!/bin/bash
echo "Uploading code to ${LAMBDA_NAME} in ${AWS_REGION} "
aws lambda update-function-code \
--function-name ${LAMBDA_NAME} \
--region ${AWS_REGION} \
--zip-file fileb://archive.zip
