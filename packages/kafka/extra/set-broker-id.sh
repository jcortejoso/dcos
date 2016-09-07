#!/bin/sh
IP=`/opt/mesosphere/bin/detect_ip`
RES=`echo $IP | sed -e 's/\.//g'`
if (( ${#RES} > 9 ));
then
    RES=`echo ${RES:${#RES}-9:9}`
fi
TEMP=${PKG_PATH}/kafka/config/server.properties.tmp
SP_PATH=${PKG_PATH}/kafka/config/server.properties
mv $SP_PATH $SP_PATH.origin
if ! grep -Fxq "reserved.broker.max.id=1000000000" $SP_PATH.origin
then
    echo "reserved.broker.max.id=1000000000" >> $SP_PATH.origin
fi
sed -e 's/broker\.id=.*/broker.id='$RES'/g' $SP_PATH.origin > $TEMP
sed -e 's/#listeners=.*/listeners=PLAINTEXT:\/\/'$IP':9092/g' $TEMP > $SP_PATH

rm -f $SP_PATH.origin
rm -f $TEMP

