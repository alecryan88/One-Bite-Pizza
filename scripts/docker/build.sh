#!/bin/bash

# Constants
AWS_ACCOUNT_ID=820242944968
REPOSITORY_NAME=one_bite_pizza_reviews
ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
FULL_REPOSITORY_NAME=$ECR_REGISTRY/$REPOSITORY_NAME
GIT_SHA=$(git rev-parse --short HEAD)


echo "Building the image"
docker build -t $FULL_REPOSITORY_NAME:main -t $FULL_REPOSITORY_NAME:$GIT_SHA .

