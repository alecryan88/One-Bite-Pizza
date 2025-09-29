#!/bin/bash

# Run build script
source ./scripts/docker/build.sh

# In dev, we mount the extract directory to the container for hot reloading
if [[ $ENV == "dev" ]]
then
    docker run --env-file .env -v $(pwd)/extract:/app/extract $GIT_TAG "$@"
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