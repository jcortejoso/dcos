#!/bin/sh
RES=`hostname -s`
SP_PATH=${PKG_PATH}/etc/telegraf-collector.conf
mv $SP_PATH $SP_PATH.origin
sed -e 's/${HOSTNAME}/'$RES'/g' $SP_PATH.origin > $SP_PATH
rm -f $SP_PATH.origin
