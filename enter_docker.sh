#!/bin/bash

set -euo pipefail

version=$(cat VERSION)
# check that version string conforms to semantic versioning
if ! [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Irregular version string: $version"
    exit 1
fi

docker run -it \
    -v "$(pwd):/workspace" \
    -v "/tmp:/tmp" \
    -w /workspace \
    "stat_gen_playground:$version" \
    bash
