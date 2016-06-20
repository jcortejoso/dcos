#!/bin/sh

cd /opt/mesosphere/packages/kafka-*
KAFKA_PATH=`pwd`

# telegraf topic exists: zookeeper is up, telegraf topic is registered
TELEGRAF_TOPIC=`$KAFKA_PATH/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --topic telegraf --describe`
if [ "$TELEGRAF_TOPIC" = "" ]; then
  echo "Topic 'telegraf' does not exist... EXITING"
  exit 1
fi


echo "Topic 'telegraf' exists... Continue..."

# telegraf znode exists
TELEGRAF_ZNODE=`echo 'ls /brokers/topics/telegraf' | $KAFKA_PATH/kafka/bin/zookeeper-shell.sh localhost:2181 | grep partitions`
if [ "$TELEGRAF_ZNODE" = "" ]; then
  echo "ZNode 'telegraf' does not exist... EXITING"
  exit 1
fi

echo "Znode 'telegraf' exists... Continue..."

# check at least this instance kafka (that is, at least this broker is available)
systemctl status kafka.service
if [ $? != 0 ]; then
  echo "Kafka service is not running... EXITING"
  exit 1
fi

# wait kakfa leadership election and other stuff...
echo "Waiting 30 secs to let kafka leadership election..."
sleep 30

#
echo "Launching telegraf-collector..."
cd /opt/mesosphere/packages/telegraf-collector-*/bin
./telegraf -config $1
