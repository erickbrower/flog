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
    """ Provides methods for signing and authenticating RESTful API requests.

    Create a new API Request like this:
   
        my_request = APIRequest()
        my_request.params['message'] = 'HORY SHET IT\'S GOJIRA'
        request.sign('MyPrivateKey123')
       
    """
    def __init__(self, json_message=None):
        self.params = {} 
        if json_message:
            self.params = json.loads(json_message)
            if not self.params: 
                raise InvalidRequestParamsError('Not a valid json message') 

    def __str__(self):
        return self._encode_params(self.params) 

    def sign(self, private_key):
        """Generates an encoded url string that contains an encrypted signature. 
        
        This hash is then set to a property on the object
        (self.params['_signature']) and returned. 
        
        Args:
            private_key: The private key used to create the request signature.

        Returns: 
            An encrypted hash of type string. 

        Raises:
            InvalidRequestParamsError: Either the _instance_key or the 
                _timestamp request params are missing.
        """
        if not self._can_be_signed():
            raise InvalidRequestParamsError(('The request params must contain' 
                ' _instance_key and _timestamp.'))
        self.params['_signature'] = self._create_signature(private_key)
        return self._encode_params(self.params)
    
    def authenticate(self, private_key):
        """Determines if the request is properly signed with the private key.

        An encrypted hash is generated using the request params and the private
        key. If the generated hash matches the request signature 
        (self.params['_signature']) then the request is authentic. 

        Args:
            private_key: The private key used to check the request signature.

        Returns:
            True if the generated hash matches the request signature, False
            if not.

        Raises:
            InvalidRequestParamsError: The _signature request param is missing.
        """
        if not self._is_signed():
            raise InvalidRequestParamsError('The request has not been signed.')
        return self._create_signature(private_key) == self.params['_signature'] 
    
    def is_valid(self):
        return self._can_be_signed()

    def _create_signature(self, private_key):
        """Creates an encrypted hash from the request params and private key.
        
        The public key is created by sorting the current request params, 
        without _signature, in alphabetical order and url encoding them. The 
        public and private keys are then used to generate a hash.

        Args:
            private_key: The private key used to create the encrypted hash.

        Returns:
            An encrypted hash of type string.
        """
        params_copy = self.params.copy()
        if '_signature' in params_copy:
            del params_copy['_signature']
        encoded_params = self._encode_params(params_copy)
        signature_digest = hmac.new(private_key, encoded_params, 
                digestmod=hashlib.sha256).digest()
        return base64.b64encode(signature_digest).decode()

    def _encode_params(self, params):
        items = params.items()
        items.sort()
        return urllib.urlencode(dict(items))

    def _is_signed(self):
        return '_signature' in self.params

    def _can_be_signed(self):
        return '_instance_key' in self.params and '_timestamp' in self.params

