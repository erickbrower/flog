import base64
import hashlib
import hmac
import urllib


class KeyMaster(object):
    PUB_KEY = '_public_key'
    SIG_KEY = '_signature'
    TIME_KEY = '_timestamp'

    @classmethod 
    def sign(cls, payload, private_key):
        if not cls.can_be_signed(payload): 
            return False
        p_copy = dict(payload.copy())
        p_copy[cls.SIG_KEY] = cls.create_signature(p_copy, private_key)
        return p_copy 

    @classmethod
    def check_keys(cls, payload, keys):
        p_key = [el for el in keys if cls.check(payload, el.key)]
        return p_key[0] if len(p_key) > 0 else False

    @classmethod
    def check(cls, payload, private_key):
        """Determines if the data is properly signed by creating a signature
        hash from the data payload and the private key, and comparing it to
        the incoming signature.

        Args:
            payload: A dictionary containing the data to be signed.
            private_key: The private key used to check the request signature.

        Returns:
            True if the generated hash matches the request signature, False
            if not.
        """
        if not cls.can_be_signed(payload):
            return False
        sig = payload.get(cls.SIG_KEY, None)
        return sig is not None and cls.create_signature(payload, private_key) \
                == payload[cls.SIG_KEY] 

    @classmethod
    def remove_keys(cls, payload):
        """Removes signature validation-related data from the payload.

        Args:
            payload: A dictionary that possibly contains signature data.

        Returns:
            A clean dictionary. So fresh!
        """
        p_copy = dict(payload.copy())
        del p_copy[cls.PUB_KEY]
        del p_copy[cls.TIME_KEY]
        del p_copy[cls.SIG_KEY]
        return p_copy

    @classmethod
    def can_be_signed(cls, payload):
        return isinstance(payload,dict) and cls.PUB_KEY in payload and cls.TIME_KEY in payload

    @classmethod
    def create_signature(cls, payload, private_key):
        """Creates a hash from the data payload and private key.
        
        The signature hash is created by sorting the current request params, 
        without the signature, in alphabetical order and url encoding them. The string
        is then hashed with the private key. 

        Args:
            payload: A dictionary containing the data to be signed. 
            private_key: The private key used to create the signature hash.

        Returns:
            A hash string.
        """
        p_copy = dict(payload.copy())
        if cls.SIG_KEY in p_copy:
            del p_copy[cls.SIG_KEY]
        items = p_copy.items()
        items.sort()
        encoded_params = urllib.urlencode(dict(items))
        signature_digest = hmac.new(private_key.encode('ascii'), encoded_params, 
                digestmod=hashlib.sha256).digest()
        return base64.b64encode(signature_digest).decode()
