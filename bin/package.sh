#!/bin/bash -e

python3 -m venv ../env

source ../env/bin/activate
./prep_local
release create first build_demo
