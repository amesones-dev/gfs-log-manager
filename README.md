# Using Google Cloud Logging to write application logs
#### Using Google Cloud resources to add Cloud logging to an app 

### Logging events to Google Cloud


Writing  logs to Google Cloud Logging services can be done  in two ways:
1. Using the Python logging handler included with the Logging client library
   1. [Connecting the Google Cloud Logging library to Python logging](https://cloud.google.com/logging/docs/setup/python#connecting_the_library_to_python_logging)
   2. [Using the Python root logger](https://cloud.google.com/logging/docs/setup/python#using_the_python_root_logger)
2. Using [Cloud Logging API Cloud client library](https://cloud.google.com/logging/docs/setup/python#use_the_cloud_client_library_directly) for Python directly.


## Recommended practice for writing app logs
* Google recommends integrating Google Cloud Logging with the standard python logging library for [writing app logs](https://cloud.google.com/appengine/docs/standard/python3/writing-application-logs#writing_app_logs).
  * Allows reusing code modules with standard python logging methods.
  * Once the Google Cloud Logging is set up to use the Python root logger, no specific code is needed to log to Google Cloud
* For apps whose specific purpose is related to Google Cloud Logging, such as application logs analytics or logging configuration, the [Google Cloud Logging API](https://cloud.google.com/logging/docs/reference/libraries) provides advanced logs manipulation methods.

## Cloud logging implementation

This demo application  uses a Google Cloud Logging handler integrated with standard python logging and uses methods form python standard logging module by 
implementing a class called GLogManager

**GLogManager**
1. Creates a Google Cloud Logging client from a service account key file  
 *Note: required IAM roles for service account: Logs Writer*
2. Creates a Google Cloud Log handler that writes logs to a Google Cloud log with a specific name defined in the 
[Flask](https://flask.palletsprojects.com/en/2.3.x/) app configuration.
4. Integrates the handler with the standard python Logging class, allowing the use of standard python logging methods whilst using Google Cloud as the logs store.
```console
     import logging
     logging.info(info_msg)
     logging.warning(warn_msg)
     logging.error(error_data) 
```

4. Also, for illustrative purposes, the class GoogleCloudManager:
* Creates a google.cloud.logging.Logger to use the Cloud Logging API directly if so desired
```console
     import google.cloud.logging 
     cloud_logger = google.cloud.logging.Logger()      
     cloud_logger.log_text(info_msg, severity='INFO')
     cloud_logger.log_text(warn_msg, severity='WARNING')
     cloud_logger.log_struct(error_data, severity='ERROR')
```
* Defines a log_example method to illustrate both ways of leveraging Google Cloud 


**Class use example to add logging to an app**  
*Link GLogManager to app*
```console
    # App specific
    # Link Google Cloud Manager to app
    gl = GLogManager()
    gl.init_app(self.app)
    # From now on, when using standard logging in the app code
    # Log messages are stored in a Google Cloud Project
    # Defined by the app configuration
```     
*Use GLogManager to log to GCP*    
```console    
    info_msg = self.app_log_id + ':starting up'
    warn_msg = self.app_log_id + ':warning message test'
    error_data = {"url": "http://test.example.com", "data": "Test error", "code": 403}

    # Logging to GCP using root Cloud Logging standard logging integration
    logging.info(info_msg)
    logging.warning(warn_msg)
    logging.error(error_data)
    
    # Logging to GCP using Cloud Logging API directly
    gl.cloud_logger.log_text(info_msg, severity='INFO')
    gl.cloud_logger.log_text(warn_msg, severity='WARNING')
    gl.cloud_logger.log_struct(error_data, severity='ERROR')
```


**App configuration keys used by GLogManager class**
```console
   # Application display name
    FLASK_APP_DISPLAY_NAME = os.environ.get('FLASK_APP_DISPLAY_NAME') or 'gcpLogDemo'
    
   # Google Cloud Logging service account key json file
   # Determines service account and hence GCP project where logs are stored
    LG_SA_KEY_JSON_FILE = os.environ.get('LG_SA_KEY_JSON_FILE') or '/etc/secrets/sa_key_lg.json'

    # Google Cloud Log configuration, preferably related to app name and environment
    # Must follow Google Cloud log names constraints
    # A new log will be created in Google Cloud Project with this name, which is  needed to search logs for this 
    # application in Logs Explorer
    GC_LOGGER_NAME = os.environ.get('GC_LOGGER_NAME') or FLASK_APP_DISPLAY_NAME
    
    # Descriptor that refers to app in logs
    APP_LOG_ID = os.environ.get('APP_LOG_ID') or FLASK_APP_DISPLAY_NAME

 ```

## Running the application locally  

### Create Google Cloud resources
1. Create a [Google Cloud](https://console.cloud.google.com/home/dashboard)  platform account if you do not already have it.
2. [Create a Google Cloud project](https://developers.google.com/workspace/guides/create-project) or use an existing one.
3. Configure application identity
   * Create a [Service Account(SA) key](https://cloud.google.com/iam/docs/keys-create-delete)
   * Assign the IAM role Logs Writer to the SA during creation.
 


### Use Google Cloud Shell
To start coding right away, launch [Google Cloud Shell](https://console.cloud.google.com/home/).  

### Or use your own development environment
If you would rather use *your own local development machine* you will need to  [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstart) and Install Python

* Install python packages.

    ```console
    sudo apt update
    sudo apt install python3 python3-dev python3-venv
    ```
    
* Install pip 

    *Note*: Debian provides a package for pip

    ```console
    sudo apt install python-pip
    ```
    Alternatively pip can be installed with the following method
    ```console
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    ```
*Note: Console snippets for Debian/Ubuntu based distributions.*
### Clone git repo from Github
At this point either you are using Cloud Shell or you have a local development environment with python and Cloud SDK.
  ```console
  git clone https://github.com/amesones-dev/gfs-log-manager.git
   ```

### Create a pyhon virtual environment

User your cloned git repository folder for your source code and Python [venv](https://docs.python.org/3/library/venv.html)
virtual environment to isolate python dependencies. 

```console
cd gfs-log-manager
python -m venv [venv-name]
source [venv-name]/bin/activate
```
Usual values for [venv-name] are `venv`, `dvenv`, `venv39` for a python 3.9 version virtual environment, etc.

### Install python requirements
```console
# From gfs-log-manager/src folder
pip install -r requirements.txt
```



### App configuration
At this point you are ready to configure and run the application.
  * Edit the application configuration Config class to update the key LG_SA_KEY_JSON_FILE with the SA key file path 
  created in  [Create Google Cloud resources](#create-google-cloud-resources)

### Running the app
  * Set Flask environment variables
   ```console
   export  FLASK_SECRET_KEY=$(openssl rand -base64 128)
   export  FLASK_APP=app:create_app
   ```

  * Run with flask
   ```console
   flask run   
   ```

  * Or run with gunicorn
   ```console
   gunicorn start:app   
   ```






