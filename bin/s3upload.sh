#!/bin/bash

BASEDIR=`dirname $0`/..
VERSION=`cat $BASEDIR/VERSION`

dcosVersion=1.8
versionPrefix=${dcosVersion}-stratio
finalVersion=${versionPrefix}${VERSION}

local_filename=dcos_generate_config.sh
filename=dcos-${finalVersion}.sh
file=/root/cd/dcos-artifacts/testing/first/${local_filename}
bucket=dcos-packages
resource="/${bucket}/${filename}"
contentType="application/x-sh"
dateValue=`date -R`
access="x-amz-acl:public-read"
stringToSign="PUT\n\n${contentType}\n${dateValue}\n${access}\n${resource}"
s3Key=${AWS_ACCESS}
s3Secret=${AWS_KEY}
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`
curl -X PUT -T "${file}" \
  -H "Date: ${dateValue}" \
  -H "Content-Type: ${contentType}" \
  -H "${access}" \
  -H "Authorization: AWS ${s3Key}:${signature}" \
  https://s3-eu-west-1.amazonaws.com${resource}