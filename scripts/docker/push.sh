#!/bin/bash

# Constants
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPOSITORY_NAME=one_bite_pizza_reviews
AWS_REGION=us-east-1
ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
FULL_REPOSITORY_NAME=$ECR_REGISTRY/$REPOSITORY_NAME

source ./scripts/docker/build.sh

echo "GIT_TAG: $GIT_TAG"
echo "MAIN_TAG: $MAIN_TAG"

# Login to ECR
echo "Logging in to ECR"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REGISTRY

# Push the image
echo "Pushing the image"
docker push $GIT_TAG
docker push $MAIN_TAG