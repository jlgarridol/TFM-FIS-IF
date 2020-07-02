#!/bin/bash
#
# Author: Mario Juez-Gil <mariojg@ubu.es>
# Spark master node init script.
#
# source: https://github.com/big-data-europe/docker-spark/blob/master/master/master.sh

set -eu pipefail

export SPARK_MASTER_HOST=$(hostname)
export SPARK_HOME=/usr/local/spark

# configuring and loading spark environment.
#. $SPARK_HOME/sbin/start-master.sh

mkdir -p $LOGS

ln -sf /dev/stdout $LOGS/stdout.log

$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master \
--ip $SPARK_MASTER_HOST --port $SPARK_PORT --webui-port $SPARK_WEBUI_PORT >> $LOGS/spark.log
