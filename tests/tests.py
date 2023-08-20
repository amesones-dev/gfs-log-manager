import unittest
import warnings

# App specific imports

# Flask App
from app import create_app
from config import TestConfig

# Cloud Logger
from glog_manager import GLogManager


class MockFSOApp:
    def __init__(self, config_class=TestConfig):
        self.config = config_class().to_dict()


class GlogManagerTestCase(unittest.TestCase):

    # Use flask_app=True  value to create a flask app with the Flask app factory create_app
    # and with test config defined in high level TestConfig
    # Creating a Flask app is needed when testing Flask related capabilities

    # Use flask_app=False to create a MockApp with config class TestFlaskAppUserConfig
    # In this case only the FlaskAppUser class and its methods are tested

    def setUp(self, flask_app=True):
        test_app = create_app(config_class=TestConfig)
        self.app = test_app

        # Flask context
        if flask_app:
            self.app_context = test_app.app_context()
            if self.app_context:
                self.app_context.push()

        # App specific
        # Link to Google Cloud Manager
        self.gl = GLogManager()
        self.gl.init_app(self.app)

        # Test logging configuration
        warnings.filterwarnings(action="ignore", category=ResourceWarning)

    def tearDown(self):
        pass

    def test_0_gl_creation_check(self):
        # Check config
        self.assertEqual(self.gl.standard_mode, self.app.config.get('GC_LOG_MODE') == 'standard')
        self.assertEqual(self.gl.app_log_id, self.app.config.get('APP_LOG_ID'))

        # Check client
        self.assertNotEqual(self.gl.client, None)
        self.assertTrue(self.gl.initialized())

        # Check handler
        self.assertNotEqual(self.gl.handler, None)




if __name__ == '__main__':
    unittest.main(verbosity=2)
