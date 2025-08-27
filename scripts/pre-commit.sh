#!/bin/bash

# Pin the runner here so devs/CI just call this script
uvx --from pre-commit==4.3.0 pre-commit "$@"