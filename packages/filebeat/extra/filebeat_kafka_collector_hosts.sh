#!/bin/bash

KAFKA_COLLECTOR_HOSTS=`cat /opt/mesosphere/etc/kafka_collector_hosts`
ROOT_CA_CERT_PATH=`cat /opt/mesosphere/etc/root_ca_cert_path`
FILEBEAT_TEMPLATE="filebeat.yml.nossl.template"

if [ -z $KAFKA_COLLECTOR_HOSTS ]
  then
  KAFKA_COLLECTOR_HOSTS="master.mesos:9092"
fi

if [ -n "$ROOT_CA_CERT_PATH" ]
    then
    FILEBEAT_TEMPLATE="filebeat.yml.ssl.template"
fi

export KAFKA_COLLECTOR_HOSTS

envsubst '$KAFKA_COLLECTOR_HOSTS' < ${PKG_PATH}/etc/$FILEBEAT_TEMPLATE > ${PKG_PATH}/etc/filebeat.yml
