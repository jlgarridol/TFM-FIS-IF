# Spark cluster test environment

Docker setup for a local spark cluster environment deployment.

## Guide and useful tips

As this repository has been created by a novel user of both, docker and spark, this section aims to be a logbook of everything discovered and learned.

### Spark master and worker

In spark there are two types of nodes, master and worker. Since the spark distribution is the same for both, docker image for master and worker will be slightly different.

The master node needs to expose up to three ports (web ui, spark master, and REST api), while the worker node only need to expose one (web ui).

### Building docker images

The dockerfiles inside `/master` and `/worker` are for building docker images with a running instance of spark framework. For start using them as docker containers, the first thing we need to do is to build the images through the command `docker build`

#### Spark Master

For building the spark master node image, we are specifying the folder containing the master node image Dockerfile. Then, with the -t parameter we are specifying the image name (spark-master) and the tag (2.4.3). I used the same tag as spark version, but docker image tag and spark version do not need to match.

```shell
[sudo] docker build ./master -t spark-master:2.4.3
```

#### Spark Worker

Analogously, spark worker image can be built with the following command:

``` shell
[sudo] docker build ./worker -t spark-worker:2.4.3
```

### Listing docker images

For obtaining the list of images we have to run the following:

```shell
[sudo] docker images
```

The output will be something like:

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
spark-worker        2.4.3               cd095ff645ba        29 minutes ago      338MB
spark-master        2.4.3               8c293e566e90        16 hours ago        338MB
alpine              latest              196d12cf6ab1        2 months ago        4.41MB
```

### Removing docker images

For removing an image we will use `docker rmi` followed the `IMAGE ID`:

For example, if we want to remove the spark-worker image of the previous example, we need to run:

```shell
[sudo] docker rmi cd095ff645ba
```

If we want to remove all docker images:

```shell
[sudo] docker rmi $([sudo] docker images -q)
```

(The `-q` parameter of `docker images` command returns a list of IDs)

**NOTE**: If a docker container is using a image, that image could not be removed until the docker container is removed.

### Running docker containers

When a image is build, the next step is to run it. The command `docker run` will be used.

#### Spark Master

The command we are using for running the spark master docker container is the following:

``` shell
[sudo] docker run -dP --name spark-master -h spark-master --cpus 1 spark-master:2.4.3
```

The explanation of the arguments used is:

* `-dP`: `d` means detached, the container will run in background. `P` is for exposing publicly all ports.
* `--name`: for setting the container name.
* `-h`: for setting the host name of the container.
* `--cpus` for setting the number of cores associated to the container
* `spark-master:2.4.3`: the docker image to run.

##### Bindmounting folders

Usually, when working with spark we are going to need to share data between host machine and the docker container.
For this purpose we can link a folder from the host machine to a folder on the container. This is called **bindmounting**.

Because we are working with spark, bindmounted folder will only be present on the master node.

The command for running the spark master docker container with a linked folder is as follows:

``` shell
[sudo] docker run -dP -v path/to/folder/inside/container:path/to/host/folder \
       --name spark-master -h spark-master --cpus 1 spark-master:2.4.3
```

* `-v`: is to configure bindmouting.

#### Spark Worker

Analogously, a spark worker can be runned like this:

``` shell                                                                                                                                              
[sudo] docker run -d --name spark-worker-01 -h spark-worker-1 --cpus 1 --link spark-master:spark-master spark-worker:2.4.3
```

The main difference is that this time we are not exposing the ports because, although it can be done, is not needed to access the workers UI (`-P` argument). Also, a new parameter `--link` was set, this is to link the worker to the master network.

### Listing docker containers

If we want to list all running docker containers, we have to use:

``` shell
[sudo] docker ps
```

The output will be something like:

```
CONTAINER ID        IMAGE                COMMAND                 CREATED             STATUS              PORTS                                                                       NAMES
388ca8feaee3        spark-worker:2.4.3   "/bin/sh -c /init.sh"   34 seconds ago      Up 33 seconds       8081/tcp                                                                    spark-worker-01
aad0b9eaab5a        spark-master:2.4.3   "/bin/bash /init.sh"    2 minutes ago       Up 2 minutes        0.0.0.0:32773->6066/tcp, 0.0.0.0:32772->7077/tcp, 0.0.0.0:32771->8080/tcp   spark-master
```

For the list of running and stopped docker containers the parameter `-a` is needed:

``` shell
[sudo] docker ps -a
```

### Stopping docker containers

For stopping (killing) a docker container, the command `docker kill` will be used.

For example, if we want to kill the docker container named `spark-master`, we have to execute:

``` shell
[sudo] docker kill spark-master
```

Instead of the container name, it can be used the container id.

### Removing docker containers

A docker container can be removed through `docker rm` command. It works similarly to the `docker rmi` shown before.

A container can be removed using its name, for example `spark-worker-01`, or its ID, for example `388ca8feaee3`. It should be used as follows:

```shell
[sudo] docker rm spark-worker-01
```

If we want to remove all containers (must be stopped), we can use the following command:

```shell
[sudo] docker rm $([sudo] docker ps -a -q)
```

Where `-a` parameter lists all docker containers (including stopped) and `-q` is for returning IDs only.

**NOTE:** If we try to remove a running container, docker will throw an error. You must kill it before, so, a more useful command for removing all containers could be:

```shell
[sudo] docker kill $([sudo] docker ps -q) && [sudo] docker rm $([sudo] docker ps -a -q)
```

### Accessing to a running docker container shell

Since a docker container is a virtual machine, can be useful to access to its shell, like a SSH connection to a remote machine. For this purpose, we can use the `docker exec` command, for example, if we want to access to the shell of the container named `spark-master`, can be done through:

```shell
[sudo] docker exec -it spark-master /bin/bash 
```

Where `-i` param means that we are running the command in interactive mode, `-t` is for attaching a TTY session, and the last `/bin/bash` refers to the shell used.
