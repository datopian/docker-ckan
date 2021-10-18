# Dockerized CKAN 
    
This repository contains base docker images, examples and docker-compose used to build and run CKAN. 

Please visit [ViderumGlobal (Deprecated)](https://github.com/ViderumGlobal/docker-ckan) repo for Dockerfiles of images using old CKAN versions

All the CKAN images are placed in their respective branch. Checkout a version. Build and tag the image and push to dockerhub.

Following are the branches for the CKAN versions
* [ckan-2.9](https://github.com/datopian/docker-ckan/tree/ckan-2.8)
* [ckan-2.8](https://github.com/datopian/docker-ckan/tree/ckan-2.8)
* [ckan-2.7](https://github.com/datopian/docker-ckan/tree/ckan-2.7)

## Usage

Following are the steps to build and push a CKAN image to dockerhub
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
