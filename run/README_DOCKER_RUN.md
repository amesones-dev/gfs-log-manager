## Local environment build of a specific feature branch
* Repo:  [gfs-log-manager](https://github.com/amesones-dev/gfs-log-manager.git).  
* Branch to build: [ci_procs](https://github.com/amesones-dev/gfs-log-manager/tree/ci_procs)
* [Dockerfile](https://github.com/amesones-dev/gfs-log-manager/blob/ci_procs/run/Dockerfile)  
* Running the application with  Flask: [start.py](https://github.com/amesones-dev/gfs-log-manager/blob/ci_procs/src/start.py)

**Dockerfile**
```Dockerfile
# Python image to use.
FROM python:3.10-alpine

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run start.py when the container launches
ENTRYPOINT ["python", "start.py"]
```
**Startup script run by docker image**
```python
# start.py
import os
from flask import Flask

from app import create_app
app = create_app()

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(host='0.0.0.0', port=int(server_port))
```

### Clone repo and checkout specific branch
**Instructions**
```shell
# Local build
REPO='https://github.com/amesones-dev/gfs-log-manager.git'
REPO_NAME='gfs-log-manager'
git clone ${REPO}
cd ${REPO_NAME}

# Select branch. Ideally use a specific convention for branch naming
export FEATURE_BRANCH="ci_procs"
# Check that the branch exists
git branch -a |grep ${FEATURE_BRANCH}

git checkout ${FEATURE_BRANCH}
# Output
    branch 'ci_procs' set up to track 'origin/ci_procs'.
    Switched to a new branch 'ci_procs'
````    

#### Build Dockerfile stored in feature branch
```shell
# Identify your build
# Usually automated CI systems provide UUID for build IDs and maintains a Build ID database
export BUILD_ID=$(python -c "import uuid;print(uuid.uuid4())")

# Use a meaningful local docker image tag
# Automated CI systems can generate a docker image tag for you
export RID="${RANDOM}-$(date +%s)" 
export LOCAL_DOCKER_IMG_TAG="${REPO_NAME}-${FEATURE_BRANCH}-${RID}"

# Launch build process with docker
# The build is done with your local environment docker engine
# docker build ./src -f ./run/Dockerfile -t ${LOCAL_DOCKER_IMG_TAG}
# With logs captured to file 
docker build . -f ./run/Dockerfile -t ${LOCAL_DOCKER_IMG_TAG} --no-cache --progress=plain  2>&1 | tee ${BUILD_ID}.log
# CI systems usually send builds to automated build engine APIs
```

#### Inspect BUILD and ARTIFACTS details
```shell
echo $BUILD_ID
# Output 
  45e4b913-dc76-4aa9-9898-217490fdd0fd

tail -n 5 "${BUILD_ID}.log"
# Output
    # 10 exporting layers
    #10 exporting layers 0.8s done
    #10 writing image sha256:a0bdb9a4065cd834549d1c2c7586c96005c1d05f0e1732e5f13edc715d62cd2b done
    #10 naming to docker.io/library/gfs-log-manager-ci_procs-24754-1691654416 done
  #10 DONE 0.8s

head -n 5 "${BUILD_ID}.log"
# Output
    # 0 building with "default" instance using docker driver
    
    #1 [internal] load build definition from Dockerfile
    #1 transferring dockerfile: 502B done
    #1 DONE 0.0s
    
    
# Artifact (docker image) details
docker image ls ${LOCAL_DOCKER_IMG_TAG}
# Output
  REPOSITORY                                  TAG       IMAGE ID       CREATED         SIZE
  gfs-log-manager-ci_procs-24754-1691654416   latest    a0bdb9a4065c   5 seconds ago   102MB
     
````

#### Run the newly built docker image
* Set container port for running application
```shell
# Default container port is 8080 if PORT not specified
export PORT=8081
export LG_SA_KEY_JSON_FILE='/etc/secrets/sa_key_lg.json'
export FLASK_SECRET_KEY=$(openssl rand -base64 128) 

# Known local path containing  SA key sa_key_lg.json
export LOCAL_SA_KEY_PATH='/secure_location'

# Set environment with -e
# Publish app port with -p 
# Mount LOCAL_SA_KEY_PATH to /etc/secrets in running container
docker run -e PORT -e LG_SA_KEY_JSON_FILE -e FLASK_SECRET_KEY -p ${PORT}:${PORT}  -v "${LOCAL_SA_KEY_PATH}":/etc/secrets  ${LOCAL_DOCKER_IMG_TAG}
```

### Watch the app running with  Web Preview
In the example, launch Web Preview on Cloud Shell, setting port to 8081.

### Inspect and test running container
*Note: Execute commands in a different Cloud Shell tab*
* Checking container is running and inspecting env

```shell
docker ps 
# Output
  # CONTAINER ID   IMAGE                                       COMMAND             CREATED         STATUS         PORTS                    NAMES
  3127ed2ef041   gfs-log-manager-ci_procs-24754-1691654416   "python start.py"   3 minutes ago   Up 3 minutes   0.0.0.0:8081->8081/tcp   beautiful_jackson

docker exec 3127ed2ef041 printenv
# Ouptut
  PORT=8081
  LG_SA_KEY_JSON_FILE=/etc/secrets/sa_key_lg.json
  ...

# Check code deployed to container from git feature branch
docker exec 3127ed2ef041 ls -R
# Output
  app
  config
  glog_manager
  requirements.txt
  start.py
  ...
  
```
* Testing endpoints
```shell
# Basic app endpoints tests
# Main url
curl --head  localhost:8081
# Output
  HTTP/1.1 200 OK
  Content-Type: text/html; charset=utf-8
  ...
  
# The app implements a /healthcheck endpoint that can be used for liveness and readiness probes
# Output set by app design
curl -i localhost:8081/healthcheck
  HTTP/1.1 200 OK
  ...
  Content-Type: application/json

  {"status":"OK"}

# Test any app endpoints as needed
export ENDPOINT='index'
curl -I  localhost:8081/${ENDPOINT}
# Output 
  HTTP/1.1 200 OK
  ...
 
curl -I -s  localhost:8081/${ENDPOINT} --output http-test-${ENDPOINT}.log
grep   'HTTP' http-test-${ENDPOINT}.log
# Output
  HTTP/1.1 200 OK

# Non existent endpoint
export ENDPOINT=app_does_not_implement
curl -I -s  localhost:8081/${ENDPOINT} --output http-test-${ENDPOINT}.log 
grep   'HTTP' http-test-${ENDPOINT}.log
# Output
  HTTP/1.1 404 NOT FOUND
   
```

```shell
# Running code integrated unittests
export TID=$(python -c "import uuid;print(uuid.uuid4())")
export LOCAL_DOCKER_IMG_TAG_TEST="test-${LOCAL_DOCKER_IMG_TAG}"


docker build . -f ./run/Dockerfile-test   -t ${LOCAL_DOCKER_IMG_TAG_TEST}  --no-cache --progress=plain  2>&1 | tee ${BUILD_ID}.log

# You may want to use a different set of environment variables to run tests
# Alternatively, code built-in tests can use a specific configuration defined inline.
export PORT=8081
export LG_SA_KEY_JSON_FILE='/etc/secrets/sa_key_lg.json'
export FLASK_SECRET_KEY=$(openssl rand -base64 128) 

# Known local path containing  SA key sa_key_lg.json
export LOCAL_SA_KEY_PATH='/secure_location'
docker run -e PORT -e LG_SA_KEY_JSON_FILE -e FLASK_SECRET_KEY -p ${PORT}:${PORT}  -v "${LOCAL_SA_KEY_PATH}":/etc/secrets  ${LOCAL_DOCKER_IMG_TAG_TEST} 2>&1 | tee ${TEST_ID}-result.log
grep 'OK' ""${TEST_ID}-result.log"" 

```

```shell
export DOCKERHUB_USER='YOUR_DOCKERHUB_USER'
export DOCKERHUB_REPO='YOUR_DOCKERIMAGE_REPO'
docker login "$DOCKERHUB_USER"

# Builds docker image
export LOCAL_TAG=${LOCAL_DOCKER_IMG_TAG}
export REMOTE_TAG="${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${LOCAL_TAG}" 

# Add remote tag to the docker image currently tag as <LOCAL_DOCKER_IMG_TAG> 
docker tag "${LOCAL__TAG}" "${REMOTE_TAG}"

# Push the image to the docker repository using the full remote tag    
docker push "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${LOCAL_TAG}"


# Tests image
export LOCAL_TAG=${LOCAL_DOCKER_IMG_TAG_TEST}
export REMOTE_TAG="${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${LOCAL_TAG}"

# Add remote tag to the docker image currently tag as <LOCAL_DOCKER_IMG_TAG> 
docker tag "${LOCAL_TAG}" "${REMOTE_TAG}"

# Push the image to the docker repository using the full remote tag    
docker push "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${LOCAL_TAG}"
```
