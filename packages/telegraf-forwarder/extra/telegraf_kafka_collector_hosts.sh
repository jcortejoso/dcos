#!/bin/bash

KAFKA_COLLECTOR_HOSTS=`cat /opt/mesosphere/etc/kafka_collector_hosts`

if [ -z $KAFKA_COLLECTOR_HOSTS ]
  then
  KAFKA_COLLECTOR_HOSTS="leader.mesos:9092"
fi

export KAFKA_COLLECTOR_HOSTS

envsubst '$KAFKA_COLLECTOR_HOSTS' < ${PKG_PATH}/etc/telegraf-forwarder.conf.template > ${PKG_PATH}/etc/telegraf-forwarder.conf
