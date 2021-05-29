# Docker

This directory contains a Dockerfile and a setup script dependency for containerization of the dIC tool.



## Build from Docker Hub

It's easiest to pull and run the newest version of the image directly from Docker Hub with the following command:

```bash
docker run -it --pull=always --rm dbdness/dic
```



 ## Build from Source

In cases of local testing and debugging, building a local image from source can be preferred. It can be done like so:

```bash
$ cd docker/
$ docker build -t dic .
```

Run the image afterwards like so:

```bash
docker run -it --rm dic
```

