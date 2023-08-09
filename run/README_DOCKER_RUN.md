
# Creating a docker artifact from a specific git repo branch (part 1 of 2)
## CI procedures introduction  
In this guide, we will introduce the foundations of 
[Continuous Integration](https://cloud.google.com/architecture/devops/devops-tech-continuous-integration)
and inspect a  basic procedure leading to automating the process of building, testing, and delivering artifacts based 
in code from specific branches in a repository:  creating a docker artifact from a specific git repo branch.
 
**CI building blocks summary**  
1. An automated build process.
   * Script that run builds and create artifacts that can be deployed to any environment.  
   * Builds can de identified, referenced and repeatable.
   * Frequent builds  
2. A suite of automated tests that must be successful as condition for artifact creation.
   * Unit tests
   * Acceptance tests
3. A CI system that runs the build and automated tests for every new version of code.
4. Small and frequent code updates to trunk-based developments, usually implemented with tools like Git and Git based 
products like GitHub, BitBucket, Cloud Repositories, etc. where code versions are organized in one or several 
environments with a main branch and feature branches that developers check out, modify and,  after automatically 
testing and passing QA tests, merge to original branches via pull requests.  
5. An agreement that when the build breaks, fixing it should take priority over any other work.  


In this case, we will inspect the basic steps for artifact building, which is the 
foundation for automating the building process.

 On this occasion, this demo will use basic tools like docker and shell are used, since the goal is to inspect the CI process itself, without focusing on a particular 
commercial solution (plus there is no GCP cost involved).  

Google Cloud has their own set of CI/CD tools, that will be considered in future posts.
* [Cloud Build](https://cloud.google.com/build/docs)
* [Cloud Deploy](https://cloud.google.com/deploy/docs)
* [Cloud Repositories](https://cloud.google.com/source-repositories/docs)
* [Artifact Registry](https://cloud.google.com/artifact-registry/docs)

 
**References**
* About [Continuous Integration](https://cloud.google.com/architecture/devops/devops-tech-continuous-integration)
by Google
'Quote' : "Continuous integration is a process in devops where changes are merged into a central repository after which the code is automated and tested."
Google CI solutions.
* [CI/CD quickstart](https://cloud.google.com/docs/ci-cd) by Google
* [Devops CI](https://cloud.google.com/architecture/devops/devops-tech-continuous-integration) by Google 
 

## Local environment build of a specific feature branch
* The example uses the repo [gfs-log-manager](https://github.com/amesones-dev/gfs-log-manager.git).  
* The [ci_procs](https://github.com/amesones-dev/gfs-log-manager/tree/ci_procs) branch contains a [Dockerfile](https://github.com/amesones-dev/gfs-log-manager/blob/ci_procs/run/Dockerfile) to build and run the application with docker engine.  
* A running docker based on the Dockerfile calls python to run the application with Flask as per [start.py](https://github.com/amesones-dev/gfs-log-manager/blob/ci_procs/src/start.py)

### Clone repo and checkout specific branch
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

### Build Dockerfile stored in feature branch
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
docker build ./src -f ./run/Dockerfile -t ${LOCAL_DOCKER_IMG_TAG}
# CI systems usually send builds to automated build engine APIs
````

### Run the newly built docker image
* Set container port for running application
```shell
# Default container port is 8080 if PORT not specified
export PORT=8081
```

* Set the local environment for the running docker image  
Usually applications expect a number of config values to be present in the running environment as variables.  
  * The demo app expects as minimal configuration the location for the Service Account(SA) key file that will identify 
  the app when accessing Cloud Logging API.  

```shell
export LG_SA_KEY_JSON_FILE='/etc/secrets/sa_key_lg.json'
```

* Run the docker image
```shell
# Known local path containing  SA key sa_key_lg.json
export LOCAL_SA_KEY_PATH='/secure_location'

# Set environment with -e
# Publish app port with -p 
# Mount LOCAL_SA_KEY_PATH to /etc/secrets in running container
docker run -e PORT=${PORT} -e LG_SA_KEY_JSON_FILE="${LG_SA_KEY_JSON_FILE}"  -p ${PORT}:${PORT}  -v "${LOCAL_SA_KEY_PATH}":/etc/secrets  ${LOCAL_BUILD_TAG}
```

###For next part of this guide (2/2)
#### Testing the application
* Defining endpoints
* Checking responses
* Running unittests in feature branch
* Note about automated testing tools

#### Upload artifact to artifact registry
* Registry tags vs local build tags
* Uploading artifact command sequence 
* Managing artifacts

#### About popular artifact registries
#### Artifacts as inputs to CI procedures  





