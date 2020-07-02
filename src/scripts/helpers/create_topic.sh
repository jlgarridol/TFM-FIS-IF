#!/bin/bash

# Create a kafka topic with 3 partitions

if [[ ! -z $1 ]]
then
	docker exec kafka_kafka_1 kafka-topics --create --topic $1 --partitions 3 --replication-factor 1 --if-not-exists --zookeeper kafka_zookeeper_1:2181
fi
