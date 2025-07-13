#!/bin/bash

set -efuo pipefail

script_dir="$(dirname "$(realpath "$0")")"
pushd "$script_dir"

version=$(cat VERSION)
# check that version string conforms to semantic versioning
if ! [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Irregular version string: $version"
    exit 1
fi

tmp_folder=$(mktemp -d)

# for poetry
poetry_venv_path="${tmp_folder}/poetry-venvs"
mkdir -p "${poetry_venv_path}"
poetry_cache_dir="${tmp_folder}/poetry-cache"
mkdir -p "${poetry_cache_dir}"

# for vscode
root_folder="${tmp_folder}/root"
mkdir -p "${root_folder}"

trap 'rm -rf "$tmp_folder"' EXIT

docker run --rm -it \
    -v "${script_dir}:/workspace" \
    -v "/tmp:/tmp" \
    -v "${poetry_venv_path}:/poetry-venvs" \
    -v "${poetry_cache_dir}:/poetry-cache" \
    -v "${root_folder}:/root" \
    -w /workspace \
    "stat_gen_playground:$version" \
    bash

popd
