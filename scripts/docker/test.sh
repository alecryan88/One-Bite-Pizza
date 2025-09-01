#!/bin/bash

ENV="dev"

if [ "$ENV" == "dev" ]; then

    echo "Do something for $ENV"

elif [ "$ENV" == "test" ]; then 

    echo "Something"

elif [ "$ENV" == "prod" ]; then
    echo "Fetch prod image from ECR. IF prod image does not exist in ECR than rebuild in dev."

else 
    echo "The environment does not exist"
    exit 0

fi