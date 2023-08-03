import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging
from google.cloud.logging_v2.handlers.transports import SyncTransport


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
            logging.log(level=log_level, msg=log_msg)
        else:
            # Logging via Cloud Logger
            self.cloud_logger.log_text(log_msg, severity=log_level)

    def init_app(self, app):
        self.standard_mode = app.config.get('GC_LOG_MODE') == 'standard'
        self.app_log_id = app.config.get('APP_LOG_ID')
        self.client = google.cloud.logging.Client.from_service_account_json(app.config.get('LG_SA_KEY_JSON_FILE'))
        self.handler = CloudLoggingHandler(self.client, name=app.config.get('GC_LOGGER_NAME'), transport=SyncTransport)

        # Set up standard logging to the lowest level for demo purposes
        logging.getLogger().setLevel(logging.INFO)  # defaults to WARN

        # Add cloud logging handler to standard logging root python logger
        setup_logging(self.handler)

        # Also, it is possible to create a logger object to use Google Cloud logger methods such as log_text, log_struct
        self.cloud_logger = google.cloud.logging.Logger(client=self.client, name=app.config.get('GC_LOGGER_NAME'))

        # https://cloud.google.com/appengine/docs/standard/python3/writing-application-logs
        # https://cloud.google.com/logging/docs/setup/python


