#!/bin/bash

poetry export -f requirements.txt --without non_docs --without-hashes --output docs/requirements.txt
