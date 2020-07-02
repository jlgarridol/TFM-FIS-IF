#!/bin/bash

NUM_WORKERS=$1

docker rm -f spark-master-fishubu &> /dev/null

i=1
while [ $i -le $NUM_WORKERS ]
do
	docker rm -f spark-worker-fishubu-$i &> /dev/null
	i=$(( $i + 1 ))
done
