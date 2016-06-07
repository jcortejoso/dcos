#!/bin/bash -e

curl -u stratio:${NEXUSPASS} --upload-file /root/cd/testing/${MODULE_VERSION}/dcos_generate_config.sh http://sodio.stratio.com/nexus/content/sites/paas/dcos/${MODULE_VERSION}/dcos_installer-${MODULE_VERSION}.sh
