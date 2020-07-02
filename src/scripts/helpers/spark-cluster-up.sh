#!/bin/bash

# arguments
HOST_DATA_DIR=$1
MASTER_CPUS=$2
NUM_WORKERS=$3
WORKER_CPUS=$4
WORKER_MEMORY=$5

ROUTE="../../dockers/spark"

# building images
if [[ "$(docker images -q spark-base-fis:2.4.5 2> /dev/null)" == "" ]]; then
  docker build $ROUTE/base -t spark-base-fis:2.4.5
  docker build $ROUTE/master -t spark-master-fis:2.4.5
  docker build $ROUTE/worker -t spark-worker-fis:2.4.5
fi

# master node
docker run -dP --mount type=bind,source="$HOST_DATA_DIR",target=/mnt/data \
  --name spark-master-fishubu \
  -h spark-master --gpus all \
  --cpus $MASTER_CPUS --network fishubu-net \
  --env PYTHONPATH="/app"\
  spark-master-fis:2.4.5

i=1
while [ $i -le $NUM_WORKERS ]
do
  docker run -dP --mount type=bind,source="$HOST_DATA_DIR",target=/mnt/data \
    --name spark-worker-fishubu-$i -h spark-worker-$i --cpus $WORKER_CPUS \
    -m $WORKER_MEMORY --network fishubu-net --gpus all\
    --env PYTHONPATH="/app"\
    spark-worker-fis:2.4.5

	i=$(( $i + 1 ))
done
