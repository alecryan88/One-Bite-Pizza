#!/bin/bash
set -euo pipefail 
# e: exit on any error
# u: treat unset variables as errors
# o pipefail: don’t ignore errors in pipelines

source ./scripts/shared/common.sh

IMAGE_TAG=${1:-latest}

aws cloudformation deploy \
    --template-file ${PWD}/infra/cloudformation/resources.yml \
    --stack-name ${PROJECT_NAME} \
    --parameter-overrides ProjectName=${PROJECT_NAME} ImageTag=${IMAGE_TAG} \
    --capabilities CAPABILITY_NAMED_IAM