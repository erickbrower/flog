import time, uuid
import unittest
from flog.key_master import KeyMaster 


class KeyMasterTest(unittest.TestCase):
    def setUp(self):
        self.payload = {u'foo': u'bar', u'turtle': u'soup', u'oh my god': u'becky' }
        self.payload[KeyMaster.PUB_KEY] = u'd0ntp4nic'
        self.payload[KeyMaster.TIME_KEY] = time.time()
        self.private_key = u'gojira'

    def test_sign_invalid_payload(self):
        self.assertFalse(KeyMaster.sign('wrongwongiswrong', 'gonnachoke'))

    def test_check_invalid_payload(self):
        self.assertFalse(KeyMaster.check('wrongwongiswrong', 'gonnachoke'))

    def test_sign_valid_payload(self):
        signed_payload = KeyMaster.sign(self.payload, self.private_key)
        self.assertIn(KeyMaster.SIG_KEY, signed_payload)

    def test_sign_invalid_payload_missing_timestamp(self):
        del self.payload[KeyMaster.TIME_KEY]
        self.assertFalse(KeyMaster.sign(self.payload, self.private_key))

    def test_sign_invalid_payload_missing_public_key(self):
        del self.payload[KeyMaster.PUB_KEY]
        self.assertFalse(KeyMaster.sign(self.payload, self.private_key))

    def test_check_keys_valid_payload_has_key(self):
        class MockHost(object):
            def __init__(self, id):
                self.id = id
        class MockKey(object):
            def __init__(self, host, key):
                self.host = host
                self.key = key
        h = MockHost(uuid.uuid1())
        keys = []
        for _ in range(10):
            keys.append(MockKey(host=h, key=str(uuid.uuid1())))
        keys.append(MockKey(host=h, key=self.private_key))
        signed = KeyMaster.sign(self.payload, self.private_key)
        self.assertTrue(KeyMaster.check_keys(signed, keys))

    def test_check_valid_request(self):
        signed_payload = KeyMaster.sign(self.payload, self.private_key)
        self.assertTrue(KeyMaster.check(signed_payload, self.private_key))

    def test_authenticate_invalid_request_invalid_private_key(self):
        signed_payload = KeyMaster.sign(self.payload, self.private_key)
        self.assertFalse(KeyMaster.check(signed_payload, 'anotherkey'))

    def test_remove_keys(self):
        all_keys = [KeyMaster.PUB_KEY, KeyMaster.SIG_KEY, KeyMaster.TIME_KEY]
        signed = KeyMaster.sign(self.payload, self.private_key)
        for key in all_keys:
            self.assertIn(key, signed)
        cleaned = KeyMaster.remove_keys(signed)
        for key in all_keys:
            self.assertNotIn(key, cleaned)
