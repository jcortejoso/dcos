#!/bin/bash

ES_CLUSTERNAME=`cat /opt/mesosphere/etc/es_clustername`

if [ -z $ES_CLUSTERNAME ]
  then
  ES_CLUSTERNAME="stratiopaas"
fi

export ES_CLUSTERNAME

sed -i "s|#cluster[.]name:.*|cluster.name: $ES_CLUSTERNAME|" "$PKG_PATH/config/elasticsearch.yml"