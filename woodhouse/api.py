import urllib
import pycurl
import hmac
import hashlib
import base64
import cStringIO
import json


class APIRequestHandler(object):
    def __init__(self, base_url, private_key):
            self.private_key = private_key
            self.base_url = base_url

    def _post(self, resource, json):
        resource_url = '{0}/{1}'.format(self.base_url, resource) 
        request = self.Request(json)
        response = self.Response() 
        c = pycurl.Curl()
        c.setopt(c.URL, resource_url)
        c.setopt(c.POSTFIELDS, request.sign(self.private_key))
        c.setopt(c.HTTPHEADER, ['Accept: application/json', 'Accept-Charset: UTF-8'])
        c.setopt(c.WRITEFUNCTION, response.write)
        c.perform()
        return response.read()
    
    class Request(object): 
        def __init__(self, json_message):
            self.value = json.loads(json_message)

        def __str__(self):
            return repr(self.value) 
        
        def sign(self, private_key):
            if '_instance_key' not in self.params or '_timestamp' not in self.params:
                raise self.InvalidQueryError('Request params must contain instance_key and timestamp')  
            items = self.params.items()
            items.sort()
            encoded_params = urllib.urlencode(dict(items))
            signature_digest = hmac.new(private_key, encoded_params, digestmod=hashlib.sha256).digest()
            return encoded_params + urllib.quote('&signature={0}'.format(base64.b64encode(signature_digest).decode()))
        
        def authenticate(self, private_key):
            if ('_instance_key' not in self.params or '_timestamp' not in self.params or 
                    '_signature' not in self.params):
               return False



    class Response(object):
        def __init__(self):
            self.content = cStringIO.StringIO
        
        def __str__(self):
            return repr(self.content.getvalue())

        def write(self, buf):
            self.content.write(buf)
        
        def read(self):
            return json.loads(self.content.getvalue())

    class InvalidQueryParameterError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)


class Woodhouse(APIRequestHandler):
    def log(self, json):
        self._post('log', json)


