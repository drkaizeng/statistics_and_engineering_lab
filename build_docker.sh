#!/bin/bash

set -eufo pipefail

script_dir="$(dirname "$(realpath "$0")")"
pushd "$script_dir"

version=$(cat VERSION)
# check that version string conforms to semantic versioning
if ! [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Irregular version string: $version"
    exit 1
fi

docker buildx build --tag "stat_gen_playground:$version" --file docker/Dockerfile .

popd
