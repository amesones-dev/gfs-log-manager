```console
REPO="https://github.com/amesones-dev/fastapi_demo.git"
TAG="fastapi_demo:v1"
git clone ${REPO}
docker build ./fastapi_demo/src/ -f ./fastapi_demo/run/Dockerfile - t ${TAG}

# Default container port is 8080 if PORT not specified
export PORT=8081


# Minimum config for BigQuery SA key
# Option 1
# Implicit app authentication to Cloud BigQuery API 
# Use GOOGLE_APP_CREDENTIALS variable if set in environment or Default Cloud running service SA
# export BQ_SA_KEY_JSON_FILE=""

# Option 2
# Explict app authentication
# If variable not defined in environment it defaults to '/etc/secrets/sa_key_bq.json'
# 
# export BQ_SA_KEY_JSON_FILE='/path_to/sa_bq_key.json'



# Alternatively mount local path with SA key to /etc/secrets
export SA_KEY_PATH='/local_path_to_SA_key_file_folder'
ls ${SA_KEY_PATH}
# Output
    sa_key_bq.json

export SA_KEY_PATH='/etc/secrets'
export BQ_SA_KEY_JSON_FILE='/etc/secrets/sa_key_bq.json'

# Mount local path to /etc/secrets when running container
docker run -p ${PORT}:${PORT} -e PORT=${PORT} -e BQ_SA_KEY_JSON_FILE="${BQ_SA_KEY_JSON_FILE}" -v "${SA_KEY_PATH}":/etc/secrets  ${TAG}

```
