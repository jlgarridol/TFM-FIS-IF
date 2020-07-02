#!/bin/bash

ID=$1

OPTIONSEMITTER="$2"
OPTIONSCONSUMER="$3"

#Necesario para nvidia
#docker exec fis-hubu-consumer-$ID rmmod nvidia_drm && rmmod nvidia_modeset && rmmod nvidia_uvm && rmmod nvidia && modprobe nvidia && modprobe nvidia_uvm && modprobe nvidia_modeset

docker exec fis-hubu-consumer-$ID /root/miniconda3/envs/default-conda/bin/python /app/consumer.py --kafkahost=kafka:9092 --ouput=/mnt --topic=video-stream-patient-$ID --sparkhost=spark://spark-master:7077 $OPTIONSCONSUMER
echo "Lanzado consumidor"
docker exec -d fis-hubu-productor-$ID /root/miniconda3/envs/default-conda/bin/python /app/producer.py --port=12345 --kafkahost=kafka:9092 --topic=video-stream-patient-$ID
echo "Lanzado productor"
docker exec -d fis-hubu-productor-$ID /root/miniconda3/envs/default-conda/bin/python /app/emitter.py --port=12345 --file=/app/testvideos/hubu-fis-3_video_1583870430.mp4 $OPTIONSEMITTER
echo "Lanzado emisor para test"



