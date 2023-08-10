

### Appendix:  how to quickly create a SA for your GCP project in CloudSDK
#### Create a service account (user managed SA)
```shell
export PROJECT_ID="YOUR_PROJECT_ID"

gcloud config set project ${PROJECT_ID}
export SA_NAME="demo-logger"
gcloud iam service-accounts create  ${SA_NAME} --description="A description" --display-name="${SA_NAME}"
```
#### Grant access to required project resources 
```shell
# SA_EMAIL follows the below format as GCP specifications
export SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
export ROLE_ID="roles/logging.logWriter"
gcloud projects add-iam-policy-binding ${PROJECT_ID}  --member="serviceAccount:${SA_EMAIL}" --role="${ROLE_ID}"
# Output
    Updated IAM policy for project [PROJECT_ID].
    bindings:
    - members:
      - serviceAccount:demo-logger@PROJECT_ID.iam.gserviceaccount.com
      role: roles/logging.logWriter
```
#### Create SA key
```shell
# Create sa key, json format by default
# Path should be a secured location 
KEY_FILE='/secure_location/sa_key_lg.json'
gcloud iam service-accounts keys create ${KEY_FILE}  --key-file-type=json --iam-account=${SA_EMAIL}
```

