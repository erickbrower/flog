from flog.models import Host
from flog.notary import Notary

class Authority(object):
    @classmethod
    def check(cls, payload):
        if Notary.public_key not in payload: 
            return False
        host = Host.objects(api_key = payload[Notary.public_key]).first()
        if host and Notary.validate(payload, host.api_private_key):
            return host
        return False
