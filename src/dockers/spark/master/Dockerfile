# Author: Mario Juez-Gil <mariojg@ubu.es>
# Spark master node Dockerfile
#
# source: https://github.com/HariSekhon/Dockerfiles/blob/master/spark/Dockerfile

FROM spark-base:2.4.5
MAINTAINER Mario Juez-Gil <mariojg@ubu.es>

# environment variables
ENV SPARK_PORT 7077
ENV SPARK_WEBUI_PORT 8080
ENV SPARK_REST_PORT 6066
ENV LOGS /logs

WORKDIR /

COPY init.sh /

EXPOSE 7077 8080 6066

CMD ["/bin/bash","/init.sh"]
