# Author: Mario Juez-Gil <mariojg@ubu.es>
# Spark standalone base Dockerfile
# https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz
#
# sources: https://github.com/HariSekhon/Dockerfiles/blob/master/spark/Dockerfile

FROM alpine:latest
MAINTAINER Mario Juez-Gil <mariojg@ubu.es>

# arguments
ARG spark_ver=2.4.5
ARG hadoop_ver=2.7
ARG tar=spark-${spark_ver}-bin-hadoop${hadoop_ver}.tgz 

# environment variables
ENV PATH $PATH:/usr/local/spark/bin

LABEL Description="Apache Spark standalone" \
    "Spark version"="${spark_ver}"

RUN set -euxo pipefail && \
    apk add --no-cache bash openjdk8-jre-base wget tar

WORKDIR /usr/local/

RUN set -euxo pipefail && \
    apk add --no-cache wget tar && \
    wget -t 100 --retry-connrefused -O "${tar}" "https://archive.apache.org/dist/spark/spark-${spark_ver}/${tar}" && \
    tar zxf "${tar}" && \
    rm -fv "${tar}" && \
    ln -s "spark-$spark_ver-bin-hadoop$hadoop_ver" spark && \
    apk del wget tar

WORKDIR /

RUN mkdir /var/run/sshd && chmod 0755 /var/run/sshd && \
cp -v /usr/local/spark/conf/spark-env.sh.template /usr/local/spark/conf/spark-env.sh