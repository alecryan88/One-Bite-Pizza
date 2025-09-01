#!/bin/bash

# Constants
AWS_ACCOUNT_ID=820242944968
IMAGE_NAME=one_bite_pizza_reviews
ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
FULL_IMAGE_NAME=$ECR_REGISTRY/$IMAGE_NAME:latest

# Login to ECR
echo "Logging in to ECR"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REGISTRY

# TODO: This error is not totally clear. The pull`` can fail for a variety of reasons.
# Return true if the image exists, false otherwise
if docker pull $FULL_IMAGE_NAME
then
    echo "Image pulled successfully"
else
    echo "Image pull failed. Building image..."
    # Build the image
    echo "Building the image"
    docker build -t $FULL_IMAGE_NAME .

    # Push the image
    echo "Pushing the image"
    docker push $FULL_IMAGE_NAME
fi


echo "Running a container"
# Run the image
docker run --pull always --env-file .env $FULL_IMAGE_NAME "$@"
