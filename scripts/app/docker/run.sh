#!/bin/bash

# Run build script
source ./scripts/app/docker/build.sh

echo "ENV: $ENV"
echo "PWD: $PWD"
echo "ECR_GIT_SHA_TAG: $ECR_GIT_SHA_TAG"
echo "ECR_ENV_TAG: $ECR_ENV_TAG"

# In dev, we mount the extract directory to the container for hot reloading
if [[ $ENV == "dev" ]]
then
    docker run --env-file .env -v $(pwd)/app:/app/app $ECR_GIT_SHA_TAG "$@"
elif [[ $ENV == "prod" ]]
then
    echo "Running in ${ENV} environment"
    echo "Pulling ${PROD_TAG}"
    docker pull $PROD_TAG
    docker run --env-file .env $ECR_GIT_SHA_TAG "$@"
else
    echo "Running in ${ENV} environment"
    docker run --env-file .env $ECR_GIT_SHA_TAG "$@"
fi