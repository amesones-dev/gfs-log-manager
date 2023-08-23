import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging
from google.cloud.logging_v2.handlers.transports import SyncTransport
import os
# https://cloud.google.com/appengine/docs/standard/python3/writing-application-logs
# https://cloud.google.com/logging/docs/setup/python


class GLogManager:

    def __init__(self):
        self.client = None
        self.handler = None
        self.app_log_id = None
        self.cloud_logger = None
        self.standard_mode = None


    def logging_example(self):

        info_msg = self.app_log_id + ':starting up'
        warn_msg = self.app_log_id + ':warning message test'
        error_data = {"url": "http://test.example.com", "data": "Test error", "code": 403}

        # Using standard logging
        logging.info(info_msg)
        logging.warning(warn_msg)
        logging.error(error_data)

        # Using google.cloud.logging_vx.logger.Logger methods
        self.cloud_logger.log_text(info_msg, severity='INFO')
        self.cloud_logger.log_text(warn_msg, severity='WARNING')
        self.cloud_logger.log_struct(error_data, severity='ERROR')

    def cloud_log(self, log_level, log_msg):
        if self.standard_mode:
            # Logging via standard logging
            levels = {'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR}
            logging.log(level=levels.get(log_level), msg=log_msg)

        else:
            # Logging via Cloud Logger
            self.cloud_logger.log_text(log_msg, severity=log_level)


        # Validates whether an app can be integrated with gbq_manager

    @staticmethod
    def validate_app(app) -> bool:
        # App: any object that has a 'config' property which is a dictionary
        # Example: could be a Flask app, a FastAPI app, etc.
        # For the app to use GLogManager as Cloud Log API manager the config must contain the following key values.

        # app.config['LG_SA_KEY_JSON_FILE']: path to Google Cloud Project Service Account credentials file.

        # Option 1. Valid path to existent  Google Cloud service account key json file
        # FROM OS or known filesystem path
        # LG_SA_KEY_JSON_FILE = os.environ.get('LG_SA_KEY_JSON_FILE') or '/etc/secrets/sa_key_lg.json'

        # Option 2. Empty string to use Google Cloud Application credentials environment
        # Default Google Cloud Application credentials
        # LG_SA_KEY_JSON_FILE = ''

        validation = False
        required = ['LG_SA_KEY_JSON_FILE', 'APP_LOG_ID', 'GC_LOG_MODE', 'GC_LOGGER_NAME']
        if 'config' in app.__dict__:
            if isinstance(app.config, dict):
                # Check mandatory config keys exist
                if set(required).issubset(app.config.keys()):
                    validation = app.config['LG_SA_KEY_JSON_FILE'] == "" \
                                 or (app.config['LG_SA_KEY_JSON_FILE'] != ""
                                     and os.path.isfile(app.config['LG_SA_KEY_JSON_FILE']))
        return validation

    # Checks a valid Clod Logging client is stored in attribute client
    def initialized(self) -> bool:
        return self.client is not None \
               and isinstance(self.client, google.cloud.logging.Client)

    def init_app(self, app):
        if self.validate_app(app):
            self.app_log_id = app.config.get('APP_LOG_ID')
            sa_creds_json_file = app.config['LG_SA_KEY_JSON_FILE']
            if sa_creds_json_file == "":
                # Use default Google Cloud application credentials or running Cloud service identity
                try:
                    self.client = google.cloud.logging.Client()
                except Exception as e:
                    logging.log(level=logging.ERROR, msg="Exception {}:{} Method: {}".format(e.__class__, e, self.init_app.__name__))
                    pass
            else:
                # Credential from file
                try:
                    self.client = google.cloud.logging.Client.from_service_account_json(sa_creds_json_file)
                except Exception as e:
                    logging.log(level=logging.ERROR,
                                msg="Exception {}:{} Method: {}".format(e.__class__, e, self.init_app.__name__))
                    pass
            if self.initialized():
                self.standard_mode = app.config.get('GC_LOG_MODE') == 'standard'
                try:
                    self.handler = CloudLoggingHandler(self.client, name=app.config.get('GC_LOGGER_NAME'),
                                                       transport=SyncTransport)
                    # Add cloud logging handler to standard logging root python logger
                    if self.standard_mode:
                        setup_logging(self.handler)
                        # Set up standard logging to the lowest level for demo purposes
                        logging.getLogger().setLevel(logging.INFO)  # defaults to WARN
                except Exception as e:
                    logging.log(level=logging.ERROR,
                                msg="Exception {}:{} Method: {}".format(e.__class__, e, self.init_app.__name__))
                    pass

            # Additionally create a logger object to use Google Cloud logger methods such as log_text, log_struct
            try:
                self.cloud_logger = google.cloud.logging.Logger(client=self.client,
                                                                name=app.config.get('GC_LOGGER_NAME'))
            except Exception as e:
                logging.log(level=logging.ERROR,
                            msg="Exception {}:{} Method: {}".format(e.__class__, e, self.init_app.__name__))
                pass

    def generate_gcp_logs_explorer_link(self):
        base_url = 'https://console.cloud.google.com/logs/'
        query_template = 'query;query=logName%3D%22projects%2FPROJECT_ID%2Flogs%2FGC_LOGGER_NAME%22;'
        return base_url + query_template.replace('PROJECT_ID', self.client.project).replace('GC_LOGGER_NAME', self.cloud_logger.name)




