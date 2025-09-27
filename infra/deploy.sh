#!/bin/bash
set -euo pipefail 
# e: exit on any error
# u: treat unset variables as errors
# o pipefail: don’t ignore errors in pipelines

PROJECT_NAME=one-bite-pizza-reviews

ENV=$1
PWD=$(pwd)

aws cloudformation deploy \
    --template-file ${PWD}/infra/resources.yml \
    --stack-name ${PROJECT_NAME}-${ENV} \
    --parameter-overrides Environment=${ENV} ProjectName=${PROJECT_NAME}




