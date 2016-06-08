#!/bin/bash

filename=dcos_generate_config.sh
file=/root/cd/dcos-artifacts/testing/first/${filename}
bucket=dcos-packages
resource="/${bucket}/${filename}"
contentType="application/x-sh"
dateValue=`date -R`
stringToSign="PUT\n\n${contentType}\n${dateValue}\n${resource}"
s3Key=${PAAS_BUCKET_ACCESS}
s3Secret=${PAAS_BUCKET_KEY}
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`
curl -X PUT -T "${file}" \
  -H "Date: ${dateValue}" \
  -H "Content-Type: ${contentType}" \
  -H "Authorization: AWS ${s3Key}:${signature}" \
  https://s3-eu-west-1.amazonaws.com${resource}
