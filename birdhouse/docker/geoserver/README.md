# docker-geoserver

A simple docker container that runs Geoserver influenced by this docker
recipe: https://github.com/eliotjordan/docker-geoserver/blob/master/Dockerfile
and modified for the PAVICS Project

The actual Geoserver is 2.9.3.
The geoserver data directory rest on the host and must be mapped on /opt/geoserver/data_dir (container)

Our Dockerfile is a modified version of
https://hub.docker.com/r/kartoza/geoserver/tags,
https://github.com/kartoza/docker-geoserver/blob/a71a2aa79315783283a33436f101857ab7eae5a4/Dockerfile.


```shell
docker build --build-arg -t pavics/geoserver . 
docker run --name "postgis" -d -t pavics/postgis:9.4-2.1

docker run --name "geoserver" --link postgis:postgis -p <host port>:8080 -v <host path to the geoserver datadir>:/opt/geoserver/data_dir -d -t pavics/geoserver

docker run --name "geoserver" --link postgis:postgis -p 8080:8080 -v /data/geoserver_data:/opt/geoserver/data_dir -d -t pavics/geoserver
```

