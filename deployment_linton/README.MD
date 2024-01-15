# Facet detection

## Build
Build docker image
```commandline
docker build -t facet-detection:v1 .
```

## Save docker image
```commandline
docker save -o <path for generated tar file> <image name>
```

## Load saved docker image
```commandline
docker load -i <path to image tar file>
```

## Run docker image
```commandline
docker run -p <host_port>:8080 -e api-source='http://192.168.73.128:8888' -v <local_mount_path>:/app/yolov5/runs  <image_name>
```
Example 
```commandline
docker run -p 8080:8080 -e api-source=cropped_stream.2.dat facet-detection:v2

docker run -p 8080:8080 -e api_source=aipngstream_endpoint.dat -e crop=True -e crop_val=375,265,30,30 -v C:\Users\mxggis\Documents\PythonScripts\SavedImages:/app/yolov5/runs/detect facet-detection:v6

```
To run docker container in background add `-d` to the above command.

## List all docker containers
```commandline
docker ps -a
```

## Stop docker container
```commandline
docker stop <container id>
```

## Remove docker container
```commandline
docker rm -f <container id>
```

## Mount docker container loc to local drive 
```commandline
docker run -p 8080:8080 -e api_source=aipngstream_endpoint.dat --mount type=bind,source=C:\Users\mxggis\Documents\PythonScripts\SavedImages\current,target=/app/yolov5/runs/detect facet-detection:v6
```

## Start container with interactive shell
```commandline
docker exec -it afb77f33b2ab /bin/bash
apt update
apt install vim


exit (to exit the container)

To make changes in the file

vim <file_name>

i (for the insert mode)
make the changes

[(control + c )/esc] ,shift+: wq (enter)
cat (to view the file)


exit (to exit the container)
docker commit <running container id> <full quailified new image name>
docker rm -f <container id>



Just to check the dir

docker exec -it afb77f33b2ab bash


<To copy the emtire contents of the container into a local dir>
The container should be running



 docker cp 2fc0fd9aaf56:/app/yolov5/runs/detect C:\Users\mxggis\Documents\PythonScripts\SavedImages 
```

