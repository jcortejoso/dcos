#!/bin/bash -e

BASEDIR=`dirname $0`/..

cd $BASEDIR

PATH=$(pwd)/dist:$PATH

# Generate combined xml
coverage combine coverage.ut coverage.it
coverage xml -o coverage-reports/overall-coverage.xml
mv .coverage coverage.overall

# Generate pylint report
pylint ssh packages pkgpanda release ssh -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt || exit 0
