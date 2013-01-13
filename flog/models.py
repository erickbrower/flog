import datetime 
from mongokit import Document, Connection

connection = Connection()
db = connection['flog_dev_mongokit']

class BaseDocument(Document):
    def save(self, uuid=False, validate=None, safe=True, *args, **kwargs):
        if hasattr(self, '_before_save') and callable(getattr(self, '_before_save')): 
            self._before_save()
        result = super(BaseDocument, self).save(uuid, validate, safe, *args, **kwargs) 
        if hasattr(self, '_after_save') and callable(getattr(self, '_after_save')): 
            self._after_save()
        return result


@connection.register
class Node(BaseDocument):

    __collection__ = 'nodes'

    structure = { 
            'name': unicode,
            'domain_ip': unicode,
            'description': unicode,
            'created': datetime.datetime,
            'modified': datetime.datetime
            }

    required_fields = ['name', 'domain_ip']

    default_values = {
            'created': datetime.datetime.utcnow,
            'modified': datetime.datetime.utcnow
            }


@connection.register
class Stream(BaseDocument):

    __collection__ = 'streams'

    structure = {
            'name': unicode,
            'description': unicode,
            'public_key': unicode,
            'private_key': unicode,
            'log_collection': unicode,
            'log_max_size_mb': int,
            'created': datetime.datetime,
            'modified': datetime.datetime,
            'node': Node
            }

    use_autorefs = True

    required_fields = ['name', 'public_key', 'private_key', 'log_collection']

    default_values = {
            'log_max_size_mb': 100,
            'created': datetime.datetime.utcnow,
            'modified': datetime.datetime.utcnow
            }


@connection.register
class Log(BaseDocument):
    structure = {
            'created': datetime.datetime
            }

    use_schemaless = True

    required_fields = ['created']

    default_values = {
            'created': datetime.datetime.utcnow
            }

