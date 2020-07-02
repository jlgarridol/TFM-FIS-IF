#!/bin/bash
#
# Author: Mario Juez-Gil <mariojg@ubu.es>
# Spark master node init script.
#
# source: https://github.com/big-data-europe/docker-spark/blob/master/worker/worker.sh

set -eu pipefail

export SPARK_HOME=/usr/local/spark

mkdir -p $LOGS

ln -sf /dev/stdout $LOGS/stdout.log

$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker \
--webui-port $SPARK_WEBUI_PORT $SPARK_MASTER >> $LOGS/spark.log
