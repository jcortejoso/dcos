#!/bin/bash -e

echo "Uploading artifact to Nexus repository"
curl -u stratio:${NEXUSPASS} --upload-file /root/cd/testing/first/dcos_generate_config.sh http://sodio.stratio.com/nexus/content/sites/paas/dcos/${MODULE_VERSION}/dcos_installer-${MODULE_VERSION}.sh

echo "Uploading artifact to s3 repository"
./s3upload.sh
