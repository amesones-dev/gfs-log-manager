import os


class Config(object):
    FLASK_APP_DISPLAY_NAME = os.environ.get('FLASK_APP_DISPLAY_NAME') or 'gcpLogDemo'
    # Recommended generating key before running server
    # export  FLASK_SECRET_KEY =$(openssl rand -base64 128 | tee /secrets_storage_path/flask_secret_key.log)
    # It generates a strong key and record its value to variable and file both

    # The Config object key for the Flask app must be called SECRET_KEY, regardless of the OS environment variable name

    # Flask Config keys and values
    # Cannot use programmatic random SECRET_KEYS with multiple gunicorn workers
    # since every worker will generate a different random key

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT') or True
    SESSION_TYPE = os.environ.get('SESSION_TYPE') or "filesystem"

    # Google Cloud Logging service account key json file
    LG_SA_KEY_JSON_FILE = os.environ.get('LG_SA_KEY_JSON_FILE') or '/etc/secrets/sa_key_lg.json'

    # Google Cloud Log configuration, preferably related to app name and environment
    # Must follow Google Cloud log names constraints
    GC_LOGGER_NAME = os.environ.get('GC_LOGGER_NAME') or FLASK_APP_DISPLAY_NAME

    # Descriptor that refers to app in logs
    APP_LOG_ID = os.environ.get('APP_LOG_ID') or FLASK_APP_DISPLAY_NAME

    # Google Cloud Logging mode
    # Set to 'standard' to integrate with Python root logger
    GC_LOG_MODE = os.environ.get('GC_LOG_MODE') or 'standard'


class TestConfig(object):
    settings = ['FLASK_APP_DISPLAY_NAME', 'LG_SA_KEY_JSON_FILE', 'GC_LOGGER_NAME', 'APP_LOG_ID', 'GC_LOG_STANDARD_MODE']
    FLASK_APP_DISPLAY_NAME = os.environ.get('FLASK_APP_DISPLAY_NAME') or 'gcpLogDemoTest'
    # Recommended generating key before running server
    # export  FLASK_SECRET_KEY =$(openssl rand -base64 128 | tee /secrets_storage_path/flask_secret_key.log)
    # It generates a strong key and record its value to variable and file both

    # The Config object key for the Flask app must be called SECRET_KEY, regardless of the OS environment variable name

    # Flask Config keys and values
    # Cannot use programmatic random SECRET_KEYS with multiple gunicorn workers
    # since every worker will generate a different random key

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT') or True
    SESSION_TYPE = os.environ.get('SESSION_TYPE') or "filesystem"

    # Google Cloud Logging service account key json file
    LG_SA_KEY_JSON_FILE = os.environ.get('LG_SA_KEY_JSON_FILE') or '/etc/secrets/sa_key_lg_test.json'

    # Google Cloud Log configuration, preferably related to app name and environment
    # Must follow Google Cloud log names constraints
    GC_LOGGER_NAME = os.environ.get('GC_LOGGER_NAME') or FLASK_APP_DISPLAY_NAME

    # Descriptor that refers to app in logs
    APP_LOG_ID = os.environ.get('APP_LOG_ID') or FLASK_APP_DISPLAY_NAME

    # Google Cloud Logging mode
    # Set to 'standard' to integrate with Python root logger
    GC_LOG_MODE = os.environ.get('GC_LOG_MODE') or 'standard'

    def to_dict(self):
        r = {}
        for k in self.settings:
            r[k] = self.__getattribute__(k)
        return r

