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
    def __init__(self, json_message=None):
        self.params = {} 
        if json_message:
            self.params = json.loads(json_message)

    def __str__(self):
        return self._encode_params(self.params) 
   
    def sign(self, private_key):
        self.params['_signature'] = self._create_signature(private_key)
    
    def authenticate(self, private_key):
        if not self._is_signed():
            raise InvalidRequestParamsError('The request was not signed by the sender')
        return self._create_signature(private_key) == self.params['_signature'] 
       
    def _create_signature(self, private_key):
        if not self._can_be_signed():
            raise InvalidRequestParamsError('The request params must contain _instance_key and _timestamp')
        params_copy = self.params.copy()
        if '_signature' in params_copy:
            del params_copy['_signature']
        encoded_params = self._encode_params(params_copy)
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

