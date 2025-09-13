#!/bin/bash

# Constants
REPOSITORY_NAME=one_bite_pizza_reviews
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=us-east-1
ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
FULL_REPOSITORY_NAME=$ECR_REGISTRY/$REPOSITORY_NAME
GIT_SHA=$GITHUB_SHA

echo "GIT_SHA: $GIT_SHA"
echo "AWS_ACCOUNT_ID: $AWS_ACCOUNT_ID"
echo "AWS_REGION: $AWS_REGION"
echo "ECR_REGISTRY: $ECR_REGISTRY"
echo "FULL_REPOSITORY_NAME: $FULL_REPOSITORY_NAME"

if [[ $ENV == "prod" ]]
then
    # Push the image
    echo "Pulling CI image"
    docker pull $FULL_REPOSITORY_NAME:ci
    echo "Re-tagging for prod"
    docker tag $FULL_REPOSITORY_NAME:ci $FULL_REPOSITORY_NAME:$ENV
    echo "Pushing to prod image to ECR"
    
    docker push $FULL_REPOSITORY_NAME:$ENV
elif [[ $ENV == "ci" ]]
then
    echo "Pushing to ECR in CI environment"
    docker push $FULL_REPOSITORY_NAME:$GIT_SHA
    docker push $FULL_REPOSITORY_NAME:$ENV
fi