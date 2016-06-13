#!/bin/bash -e

echo "Uploading artifact to Nexus repository"
curl -u stratio:${NEXUSPASS} --upload-file /root/cd/dcos-artifacts/testing/first/dcos_generate_config.sh http://sodio.stratio.com/nexus/content/sites/paas/dcos/${MODULE_VERSION}/stratio-dcos-${MODULE_VERSION}.sh

echo "Uploading artifact to s3 repository"
bin/s3upload.sh
