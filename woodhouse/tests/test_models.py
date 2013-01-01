from woodhouse.app import app
from woodhouse.models import Application, Log
from flask.ext.mongoengine import ValidationError
from factories import ApplicationFactory, LogFactory
import unittest


class ApplicationModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True

    def tearDown(self):
        Application.drop_collection()
        Log.drop_collection()


    def test_should_have_attributes(self):
        application = ApplicationFactory()
        assert hasattr(application, 'name')
        assert hasattr(application, 'instance')
        assert hasattr(application, 'description')
        assert hasattr(application, 'api_key')
        assert hasattr(application, 'api_private_key')
        assert hasattr(application, 'created')

    def test_should_require_name(self):
        application = ApplicationFactory()
        application.name = None
        with self.assertRaises(ValidationError):
            application.validate()

    def test_should_require_api_key(self):
        application = ApplicationFactory()
        application.api_key = None
        with self.assertRaises(ValidationError):
            application.validate()

    def test_should_require_api_private_key(self):
        application = ApplicationFactory()
        application.api_private_key = None
        with self.assertRaises(ValidationError):
            application.validate()


class LogModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True

    def tearDown(self):
        Application.drop_collection()
        Log.drop_collection()

    def test_should_have_attributes(self):
        log = LogFactory.build()
        assert hasattr(log, 'content')
        assert hasattr(log, 'application')
        assert hasattr(log, 'created')

    def test_should_require_application(self):
        log = LogFactory()
        log.application = None
        with self.assertRaises(ValidationError):
            log.validate()
