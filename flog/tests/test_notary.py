import unittest
import time
from flog.lib.notary import Notary


class NotaryTest(unittest.TestCase):
    def setUp(self):
        self.payload = {'_timestamp': time.time(), '_api_key': 'd0ntp4nic', 'foo': 'bar', 'turtle': 'soup'}
        self.private_key = 'gojira'

    def test_sign_invalid_payload(self):
        self.assertFalse(Notary.sign('wrongwongiswrong', 'gonnachoke'))

    def test_validate_invalid_payload(self):
        self.assertFalse(Notary.validate('wrongwongiswrong', 'gonnachoke'))

    def test_sign_valid_payload(self):
        signed_payload = Notary.sign(self.payload, self.private_key)
        self.assertIn('_signature', signed_payload)

    def test_sign_invalid_payload_missing_timestamp(self):
        del self.payload['_timestamp']
        self.assertFalse(Notary.sign(self.payload, self.private_key))

    def test_sign_invalid_payload_missing_api_key(self):
        del self.payload['_api_key']
        self.assertFalse(Notary.sign(self.payload, self.private_key))

    def test_authenticate_valid_request(self):
        signed_payload = Notary.sign(self.payload, self.private_key)
        self.assertTrue(Notary.validate(signed_payload, self.private_key))

    def test_authenticate_invalid_request_invalid_private_key(self):
        signed_payload = Notary.sign(self.payload, self.private_key)
        self.assertFalse(Notary.validate(signed_payload, 'anotherkey'))
