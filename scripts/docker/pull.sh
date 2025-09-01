#!/bin/bash

# Constants
AWS_ACCOUNT_ID=820242944968
REPOSITORY_NAME=one_bite_pizza_reviews
ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
FULL_REPOSITORY_NAME=$ECR_REGISTRY/$REPOSITORY_NAME

# Login to ECR
echo "Logging in to ECR"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REGISTRY

# Pull the image
if docker pull $FULL_REPOSITORY_NAME:latest
then
    echo "Image pulled successfully"
else
    echo "Image does not exist. Building image..."
    # Build the image
    echo "Building the image"
    docker build -t $FULL_REPOSITORY_NAME:latest .

    # Push the image
    echo "Pushing the image"
    docker push $FULL_REPOSITORY_NAME:latest
fi