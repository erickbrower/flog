from flog import app
from flog.models import db
from mongokit import RequireFieldError
import unittest, uuid

def node_factory():
    node = db.Node()
    node['name'] = u'Test Node %s' % uuid.uuid1()
    node['domain_ip'] = u'erickbrower.org'
    node['description'] = u'Things and stuff.'
    return node

def stream_factory():
    stream = db.Stream()
    stream['name'] = u'Test Log Stream %s' % uuid.uuid1()
    stream['description'] = u'This is a test!'
    stream['public_key'] = u'mickey'
    stream['private_key'] = unicode(uuid.uuid1())
    stream['log_collection'] = u'test_%s' % uuid.uuid1()
    stream['log_max_size_mb'] = 50
    return stream

def log_factory(collection):
    log = db[collection].Log()
    log['walk'] = u'hard'
    log['guilty'] = u'as charged'
    return log


class NodeModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.node = node_factory()

    def tearDown(self):
        db.drop_collection('nodes')

    def test_should_save(self):
        self.node.save()
        node = db.Node.find_one({u'domain_ip': u'erickbrower.org'})
        assert node is not None

    def test_should_retrieve(self):
        self.node.save()

    def test_should_have_attributes(self):
        attrs = ('name', 'domain_ip', 'description', 'created', 'modified')
        for attr in attrs:
            assert attr in self.node

    def test_should_require_name(self):
        self.node['name'] = None
        with self.assertRaises(RequireFieldError):
            self.node.save()

    def test_should_require_domain_ip(self):
        self.node['domain_ip'] = None
        with self.assertRaises(RequireFieldError):
            self.node.save()


class StreamModelTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.node = node_factory()
        self.node.save()
        self.stream = stream_factory()
        self.stream.node = self.node

    def tearDown(self):
        db.drop_collection('streams')
        db.drop_collection('nodes')

    def test_should_save(self):
        self.stream.save()

    def test_should_retrieve(self):
        self.stream.save()
        stream = db.Stream.find_one({u'public_key': u'mickey'})
        assert stream is not None

    def test_should_have_attributes(self):
        attrs = (u'name', u'description', u'public_key', u'private_key', \
                u'log_collection', u'log_max_size_mb', u'created', u'modified', \
                u'node')
        for attr in attrs:
            assert attr in self.stream

    def test_should_require_name(self):
        self.stream[u'name'] = None
        with self.assertRaises(RequireFieldError):
            self.stream.save()

    def test_should_require_public_key(self):
        self.stream[u'public_key'] = None
        with self.assertRaises(RequireFieldError):
            self.stream.save()

    def test_should_require_private_key(self):
        self.stream[u'private_key'] = None
        with self.assertRaises(RequireFieldError):
            self.stream.save()

    def test_should_require_log_collection(self):
        self.stream[u'log_collection'] = None
        with self.assertRaises(RequireFieldError):
            self.stream.save()


class LogModelTesT(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.node = node_factory()
        self.node.save()
        self.stream = stream_factory()
        self.stream.node = self.node
        self.stream.save()
        self.log = log_factory(self.stream[u'log_collection'])

    def tearDown(self):
        db.drop_collection(self.stream[u'log_collection'])

    def test_should_save(self):
        self.log.save()

    def test_should_have_attributes(self):
        assert 'created' in self.log

    def test_should_retrieve(self):
        self.log.save()
        log = db[self.stream[u'log_collection']].Log.find_one({u'walk':u'hard'})
        assert log is not None
