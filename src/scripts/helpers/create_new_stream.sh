#!/bin/bash

# Lanzar desde deploy

OPTIONSEMITTER="$1"
OPTIONSCONSUMER="$2"
OUTPUT="/mnt/data"

if [[ "$(docker images -q fishubu-base:1.0.0 2> /dev/null)" == "" ]]; then
    docker build -f ../../dockers/fishubu/base/Dockerfile -t fishubu-base:1.0.0 ../../
    docker build -f ../../dockers/fishubu/enviroment/Dockerfile -t fishubu-env:1.0.0 ../../
fi


aux=$(ls /tmp/flush.* 2> /dev/null | cut -f 2 -d"." | sort -nr | head -n1)

if [ -z $aux ]; then
    aux=0
else
    let aux++
fi

touch /tmp/flush.$aux

bash ../helpers/create_topic.sh video-stream-patient-$aux

docker run -dP \
  --name fis-hubu-productor-$aux \
  --cpus 1 --network fishubu-net --gpus all\
  fishubu-env:1.0.0

docker run -dP \
  --name fis-hubu-consumer-$aux \
  --mount type=bind,source="$OUTPUT",target=/mnt \
  --cpus 1 --network fishubu-net --gpus all\
  fishubu-env:1.0.0

bash ../helpers/launch_stream.sh $aux "$OPTIONSEMITTER" "$OPTIONSCONSUMER"

echo "Se ha lanzado un nuevo flujo. Su identificador es: $aux"