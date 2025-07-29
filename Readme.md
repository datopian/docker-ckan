# Dockerized CKAN 
    
This repository contains base docker images, examples and docker-compose used to build and run CKAN. 

Please visit [ViderumGlobal (Deprecated)](https://github.com/ViderumGlobal/docker-ckan) repo for Dockerfiles of images using old CKAN versions

All the CKAN images are placed in their respective branch. Checkout a version. Build and tag the image and push to dockerhub.

You can find the existing image tags on [DockerHub](https://hub.docker.com/r/viderum/ckan/tags).

## Usage

* Tag the changes to a specific version
* Push the tag to this repo
* Build the dockerfile
  ```
  make build
  ```
* Push the image to dockerhub
  ```
  make push
  ```