#!/bin/bash

# Run build script
source ./scripts/docker/build.sh

# In dev, we mount the extract directory to the container for hot reloading
if [[ $ENV == "dev" ]]
then
    docker run --env-file .env -v $(pwd)/extract:/app/extract $GIT_TAG "$@"
else
    echo "Running in ${ENV} environment"
    docker run $GIT_TAG "$@"
fi