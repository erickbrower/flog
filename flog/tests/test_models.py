from flog import app
from flog.models import Host, Log, User 
from flask.ext.mongoengine import ValidationError
from factories import HostFactory, LogFactory, UserFactory, KeyRingFactory, KeyFactory
import unittest


class HostModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.host = HostFactory()

    def tearDown(self):
        Host.drop_collection()

    def test_should_have_attributes(self):
        assert hasattr(self.host, 'name')
        assert hasattr(self.host, 'description')
        assert hasattr(self.host, 'created')

    def test_should_require_name(self):
        self.host.name = None
        with self.assertRaises(ValidationError):
            self.host.validate()


class LogModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.log = LogFactory.build()

    def tearDown(self):
        Host.drop_collection()
        Log.drop_collection()

    def test_should_have_attributes(self):
        assert hasattr(self.log, 'host')
        assert hasattr(self.log, 'created')

    def test_should_require_host(self):
        self.log.host = None
        with self.assertRaises(ValidationError):
            self.log.validate()


class UserModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.user = UserFactory.build()

    def tearDown(self):
        User.drop_collection()

    def test_should_have_attributes(self):
        assert hasattr(self.user, 'email_address')
        assert hasattr(self.user, 'password_hash')
        assert hasattr(self.user, 'created')

    def test_should_require_email_address(self):
        self.user.email_address = None
        with self.assertRaises(ValidationError):
            self.user.validate()

    def test_should_require_password_hash(self):
        self.user.password_hash = None
        with self.assertRaises(ValidationError):
            self.user.validate()


class KeyModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.key = KeyFactory.build()

    def test_should_have_attributes(self):
        assert hasattr(self.key, 'host')
        assert hasattr(self.key, 'key')


class KeyRingModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.keyring = KeyRingFactory.build()

    def test_should_have_attributes(self):
        assert hasattr(self.keyring, 'user')
        assert hasattr(self.keyring, 'keys')

