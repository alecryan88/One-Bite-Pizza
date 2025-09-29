#!/bin/bash

# Run build script
source ./scripts/app/docker/build.sh

echo "ENV: $ENV"
echo "GIT_TAG: $GIT_TAG"
echo "PROD_TAG: $PROD_TAG"
echo "PWD: $PWD"

# In dev, we mount the extract directory to the container for hot reloading
if [[ $ENV == "dev" ]]
then
    docker run --env-file .env -v $(pwd)/app:/app/app $GIT_TAG "$@"
elif [[ $ENV == "prod" ]]
then
    echo "Running in ${ENV} environment"
    echo "Pulling ${PROD_TAG}"
    docker pull $PROD_TAG
    docker run --env-file .env $PROD_TAG "$@"
else
    echo "Running in ${ENV} environment"
    docker run --env-file .env $GIT_TAG "$@"
fi