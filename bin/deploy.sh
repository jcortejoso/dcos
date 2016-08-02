#!/bin/bash -e

BASEDIR=`dirname $0`/..
VERSION=`cat $BASEDIR/VERSION`

dcosVersion=1.8
versionPrefix=${dcosVersion}-stratio
finalVersion=${versionPrefix}${VERSION}

echo "Uploading artifact to Nexus repository"
curl -u stratio:${NEXUSPASS} --upload-file /root/cd/dcos-artifacts/testing/first/dcos_generate_config.sh http://sodio.stratio.com/nexus/content/sites/paas/dcos/${finalVersion}/dcos-${finalVersion}.sh

echo "Uploading artifact to s3 repository"
bin/s3upload.sh
