#!/bin/bash

# Constants
AWS_ACCOUNT_ID=820242944968
IMAGE_NAME=one_bite_pizza_reviews
ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Login to ECR
echo "Logging in to ECR"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REGISTRY

# Build the image
echo "Building the image"
docker build -t $IMAGE_NAME .

# Tag the image
echo "Tagging the image"
docker tag $IMAGE_NAME:latest $ECR_REGISTRY/$IMAGE_NAME:latest

# Push the image
echo "Pushing the image"
docker push $ECR_REGISTRY/$IMAGE_NAME:latest