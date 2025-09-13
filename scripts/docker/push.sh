#!/bin/bash

# Constants
AWS_ACCOUNT_ID=820242944968 #$(aws sts get-caller-identity --query Account --output text)
REPOSITORY_NAME=one_bite_pizza_reviews
AWS_REGION=us-east-1
ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
FULL_REPOSITORY_NAME=$ECR_REGISTRY/$REPOSITORY_NAME
GIT_SHA=$GITHUB_SHA

echo "GIT_SHA: $GIT_SHA"
echo "MAIN_TAG: $MAIN_TAG"

# Push the image
echo "Pushing the image"
docker push $FULL_REPOSITORY_NAME:$GIT_SHA
docker push $FULL_REPOSITORY_NAME:ci