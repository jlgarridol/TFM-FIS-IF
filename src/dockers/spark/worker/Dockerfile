# Author: Mario Juez-Gil <mariojg@ubu.es>
# Spark worker node Dockerfile
#
# source: https://github.com/HariSekhon/Dockerfiles/blob/master/spark/Dockerfile

FROM spark-base:2.4.5
MAINTAINER Mario Juez-Gil <mariojg@ubu.es>

# environment variables
ENV SPARK_WEBUI_PORT 8081
ENV SPARK_MASTER "spark://spark-master:7077"
ENV LOGS /logs

WORKDIR /

COPY init.sh /

EXPOSE 8081

CMD ["/bin/bash","/init.sh"]
