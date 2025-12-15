#!/bin/bash

poetry export -f requirements.txt --without non_docs --without-hashes --output requirements.txt
