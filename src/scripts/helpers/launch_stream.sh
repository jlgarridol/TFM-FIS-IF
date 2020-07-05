#!/bin/bash

ID=$1

OPTIONSEMITTER="$2"
OPTIONSCONSUMER="$3"

#Necesario para nvidia
#docker exec fis-hubu-consumer-$ID rmmod nvidia_drm && rmmod nvidia_modeset && rmmod nvidia_uvm && rmmod nvidia && modprobe nvidia && modprobe nvidia_uvm && modprobe nvidia_modeset

docker exec -d fis-hubu-consumer-$ID /bin/bash -c "cd app && /root/miniconda3/envs/default-conda/bin/python consumer.py --kafkahost='kafka_kafka_1:29092' --output=/mnt/data --topic=video-stream-patient-$ID --sparkhost='spark://spark-master-fishubu:7077' $OPTIONSCONSUMER >> /mnt/data/log-$ID 2> /mnt/data/log-error-$ID"
echo 'Lanzado consumidor'
docker exec -d fis-hubu-productor-$ID /bin/bash -c "cd app && /root/miniconda3/envs/default-conda/bin/python producer.py --port=12345 --kafkahost='kafka_kafka_1:29092' --topic=video-stream-patient-$ID"
echo 'Lanzado productor'
docker exec -d fis-hubu-productor-$ID /bin/bash -c "cd app && /root/miniconda3/envs/default-conda/bin/python emitter.py --port=12345 --file=/app/testvideos/sentado2-cruzado.mp4 $OPTIONSEMITTER"
echo 'Lanzado emisor para test'




