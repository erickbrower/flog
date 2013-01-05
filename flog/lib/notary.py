import base64
import hashlib
import hmac
import urllib


class Notary(object):
    public_key = '_api_key'
    timestamp_key = '_timestamp'
    signature_key = '_signature'

    @classmethod 
    def sign(cls, payload, private_key):
        if not cls._can_be_signed(payload): 
            return False
        payload[cls.signature_key] = cls._create_signature(payload, private_key)
        return payload

    @classmethod
    def validate(cls, payload, private_key):
        """Determines if the data is properly signed by creating a signature
        hash from the data payload and the private key, and comparing it to
        the incoming signature.

        Args:
            payload: A dictinoary containing the data to be signed.
            private_key: The private key used to check the request signature.

        Returns:
            True if the generated hash matches the request signature, False
            if not.

        Raises:
            InvalidRequestParamsError: The _signature request param is missing.
        """
        if cls.signature_key not in payload:
            return False
        return cls._create_signature(payload, private_key) == unicode(payload[cls.signature_key]) 

    @classmethod
    def clean(cls, payload):
        """Removes signature validation-related data from the payload.

        Args:
            payload: A dictionary that possibly contains signature data.

        Returns:
            A clean dictionary. So fresh!
        """
        p_copy = dict(payload.copy())
        del p_copy[cls.public_key]
        del p_copy[cls.timestamp_key]
        del p_copy[cls.signature_key]
        return p_copy

    @classmethod
    def _can_be_signed(cls, payload):
        return cls.public_key in payload and cls.timestamp_key in payload

    @classmethod
    def _create_signature(cls, payload, private_key):
        """Creates a hash from the data payload and private key.
        
        The signature hash is created by sorting the current request params, 
        without _signature, in alphabetical order and url encoding them. The string
        is then hashed with the private key. 

        Args:
            payload: A dictionary containing the data to be signed. 
            private_key: The private key used to create the signature hash.

        Returns:
            A hash string.
        """
        p_copy = dict(payload.copy())
        if cls.signature_key in p_copy:
            del p_copy[cls.signature_key]
        items = p_copy.items()
        items.sort()
        encoded_params = urllib.urlencode(dict(items))
        signature_digest = hmac.new(private_key.encode('ascii'), encoded_params, 
                digestmod=hashlib.sha256).digest()
        return unicode(base64.b64encode(signature_digest).decode())
