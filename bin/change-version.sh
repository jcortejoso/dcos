#!/bin/bash -e

BASEDIR=`dirname $0`/..

cd $BASEDIR

PATH=$(pwd)/dist:$PATH

echo "Modifying version to: $1"
echo $1 > VERSION
