import base64
import hashlib
import hmac
import urllib
import copy


class ApiRequestAuthority(object):
    @classmethod 
    def sign(cls, payload, private_key):
        if not isinstance(payload, dict):
            raise ValueError('Payload must be of type dict')
        if not cls._can_be_signed(payload): 
            raise ValueError('Payload must contain _api_key and \
                    _timestamp in order to be properly signed.')
        payload['_signature'] = cls._create_signature(payload, private_key)
        return payload

    @classmethod
    def validate(cls, payload, private_key):
        """Determines if the request is properly signed with the private key.

        A hash is generated using the request params and the private
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
        if not isinstance(payload, dict):
            raise ValueError('Payload must be of type dict')
        if not '_signature' in payload:
            raise ValueError('The request has not been signed.')
        return cls._create_signature(payload, private_key) == unicode(payload['_signature']) 


    @classmethod
    def _can_be_signed(cls, payload):
        return '_api_key' in payload and '_timestamp' in payload

    @classmethod
    def _create_signature(cls, payload, private_key):
        """Creates an hash from the request params and private key.
        
        The public key is created by sorting the current request params, 
        without _signature, in alphabetical order and url encoding them. The 
        public and private keys are then used to generate a hash.

        Args:
            private_key: The private key used to create the signature hash.

        Returns:
            An hash of type string.
        """
        payload_copy = dict(payload.copy())
        if '_signature' in payload_copy:
            del payload_copy['_signature']
        items = payload_copy.items()
        items.sort()
        encoded_params = urllib.urlencode(dict(items))
        signature_digest = hmac.new(private_key.encode('ascii'), encoded_params, 
                digestmod=hashlib.sha256).digest()
        return unicode(base64.b64encode(signature_digest).decode())

