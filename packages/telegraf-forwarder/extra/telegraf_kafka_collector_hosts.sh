#!/bin/bash

KAFKA_COLLECTOR_HOSTS=`cat /opt/mesosphere/etc/kafka_collector_hosts`
ROOT_CA_CERT_PATH=`cat /opt/mesosphere/etc/root_ca_cert_path`
TELEGRAF_FORWARDER_TEMPLATE="telegraf-forwarder.conf.template"

if [ -z $KAFKA_COLLECTOR_HOSTS ]
  then
  KAFKA_COLLECTOR_HOSTS=`cat /opt/mesosphere/etc/kafka_collector_hosts_internal`
  if [ -z $KAFKA_COLLECTOR_HOSTS ]
  then
    KAFKA_COLLECTOR_HOSTS="master.mesos:9092"
  fi
fi

if [ -n "$ROOT_CA_CERT_PATH" ]
    then
    TELEGRAF_FORWARDER_TEMPLATE="telegraf-forwarder.conf.ssl.template"
fi

export KAFKA_COLLECTOR_HOSTS
export ROOT_CA_CERT_PATH

TELEGRAF_FORWARDER_TEMPLATE_AUX="telegraf-forwarder.conf.aux.template"

envsubst '$KAFKA_COLLECTOR_HOSTS' < ${PKG_PATH}/etc/$TELEGRAF_FORWARDER_TEMPLATE > \
${PKG_PATH}/etc/$TELEGRAF_FORWARDER_TEMPLATE_AUX

envsubst '$ROOT_CA_CERT_PATH' < ${PKG_PATH}/etc/$TELEGRAF_FORWARDER_TEMPLATE_AUX > \
${PKG_PATH}/etc/telegraf-forwarder.conf

rm -f ${PKG_PATH}/etc/$TELEGRAF_FORWARDER_TEMPLATE_AUX
