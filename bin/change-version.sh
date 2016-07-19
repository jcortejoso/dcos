#!/bin/bash -e

BASEDIR=`dirname $0`/..

cd $BASEDIR

PATH=$(pwd)/dist:$PATH

echo "Modifying version to: $1"
echo $1 > VERSION
sed -i "s|stratiopaas_version.*|stratiopaas_version': '"$1"'|" gen/calc.py
