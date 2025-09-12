#!/bin/bash

# Constants
AWS_ACCOUNT_ID=820242944968 #$(aws sts get-caller-identity --query Account --output text)
REPOSITORY_NAME=one_bite_pizza_reviews
ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
FULL_REPOSITORY_NAME=$ECR_REGISTRY/$REPOSITORY_NAME
GIT_SHA=$(git rev-parse --short HEAD)

if [[ $ENV == "dev" ]]
then
    # Tags image with the git sha, no main tag. This is used for quick development and testing.
    echo "Building the image in ${ENV} environment"
    docker build -t $REPOSITORY_NAME:$GIT_SHA -f Dockerfile .

elif [[ $ENV == "ci" ]]
then
    # Tags image with the git sha, and  ci tag. This is used for CI only.
    echo "Building the image in ${ENV} environment"
    docker build -t $FULL_REPOSITORY_NAME:ci -t $FULL_REPOSITORY_NAME:$GIT_SHA -f Dockerfile .


elif [[ $ENV == "prod" ]]
then
    # Tags image with the main tag and the git sha in prod
    echo "Building the image in ${ENV} environment"
    docker build -t $FULL_REPOSITORY_NAME:main -t $FULL_REPOSITORY_NAME:$GIT_SHA -f Dockerfile .
    
else
    echo "This is not a valid environment. Use dev, ci, or prod."
fi


export GIT_TAG=$FULL_REPOSITORY_NAME:$GIT_SHA
export MAIN_TAG=$FULL_REPOSITORY_NAME:main