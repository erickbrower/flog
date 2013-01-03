import factory
from flog.models import Host, Log, User

class HostFactory(factory.Factory):
    FACTORY_FOR = Host

    name = factory.Sequence(lambda n: 'Test Application {0}'.format(n))
    instance = 'test'
    api_key = factory.Sequence(lambda n: 'key_{0}'.format(n))
    api_private_key = factory.Sequence(lambda n: 'private_key_{0}'.format(n))
    description = 'This is a test description!'


class LogFactory(factory.Factory):
    FACTORY_FOR = Log

    content = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    host = factory.SubFactory(HostFactory)


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    email_address = factory.Sequence(lambda n: 'emailaddress{0}@test.com'.format(n))
    password_hash = '12345678'

