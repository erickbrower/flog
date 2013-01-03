from flog import app
from flog.models import Host, Log, User 
from flask.ext.mongoengine import ValidationError
from factories import HostFactory, LogFactory, UserFactory
import unittest


class HostModelTest(unittest.TestCase):
    def setUp(sejf):
        app.config['TESTING'] = True

    def tearDown(self):
        Host.drop_collection()
        Log.drop_collection()


    def test_should_have_attributes(self):
        host = HostFactory()
        assert hasattr(host, 'name')
        assert hasattr(host, 'instance')
        assert hasattr(host, 'description')
        assert hasattr(host, 'api_key')
        assert hasattr(host, 'api_private_key')
        assert hasattr(host, 'created')

    def test_should_require_name(self):
        host = HostFactory()
        host.name = None
        with self.assertRaises(ValidationError):
            host.validate()

    def test_should_require_api_key(self):
        host = HostFactory()
        host.api_key = None
        with self.assertRaises(ValidationError):
            host.validate()

    def test_should_require_api_private_key(self):
        host = HostFactory()
        host.api_private_key = None
        with self.assertRaises(ValidationError):
            host.validate()


class LogModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True

    def tearDown(self):
        Host.drop_collection()
        Log.drop_collection()

    def test_should_have_attributes(self):
        log = LogFactory.build()
        assert hasattr(log, 'content')
        assert hasattr(log, 'host')
        assert hasattr(log, 'created')

    def test_should_require_host(self):
        log = LogFactory()
        log.host = None
        with self.assertRaises(ValidationError):
            log.validate()


class UserModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True

    def tearDown(self):
        User.drop_collection()

    def test_should_have_attributes(self):
        user = UserFactory.build()
        assert hasattr(user, 'email_address')
        assert hasattr(user, 'password_hash')
        assert hasattr(user, 'created')

    def test_should_require_email_address(self):
        user = UserFactory.build()
        user.email_address = None
        with self.assertRaises(ValidationError):
            user.validate()

    def test_should_require_password_hash(self):
        user = UserFactory.build()
        user.password_hash = None
        with self.assertRaises(ValidationError):
            user.validate()
