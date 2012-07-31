import urllib
import hmac
import hashlib
import base64
import json


class InvalidRequestParamsError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

   
class APIRequest(object): 
    def __init__(self, json_message):
        self.params = json.loads(json_message)

    def __str__(self):
        return self._encoded_params() 
   
    def sign(self, private_key):
        self.params['_signature'] = self._create_signature(private_key)
    
    def authenticate(self, private_key):
        if not self._is_signed():
            raise InvalidRequestParamsError('_signature is missing from request params')
        client_signature = self.params['_signature']
        return self._create_signature(private_key) == client_signature
       
    def _create_signature(self, private_key):
        if not self._can_be_signed():
            raise InvalidRequestParamsError('Request params must contain _instance_key and _timestamp')
        current_params = self.params
        if self._is_signed():
            del current_params['_signature']
        encoded_params = self._encode_params(current_params)
        signature_digest = hmac.new(private_key, encoded_params, digestmod=hashlib.sha256).digest()
        return base64.b64encode(signature_digest).decode()

    def _encode_params(self, params):
        items = params.items()
        items.sort()
        return urllib.urlencode(dict(items))

    def _is_signed(self):
        return '_signature' in self.params

    def _can_be_signed(self):
        return '_instance_key' in self.params and '_timestamp' in self.params

