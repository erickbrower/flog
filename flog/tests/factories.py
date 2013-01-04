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
    field1 = factory.Sequence(lambda n: 'value {0}'.format(n))
    field2 = factory.Sequence(lambda n: 'value {0}'.format(n))
    van = 'halen'
    foo = 'bar'
    stuff = 'thing'
    host = factory.SubFactory(HostFactory)


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    email_address = factory.Sequence(lambda n: 'emailaddress{0}@test.com'.format(n))
    password_hash = '12345678'

