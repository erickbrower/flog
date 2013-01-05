import factory
from flog.models import Host, Log, User, Key, KeyRing

class HostFactory(factory.Factory):
    FACTORY_FOR = Host

    name = factory.Sequence(lambda n: 'Test Application {0}'.format(n))
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


class KeyFactory(factory.Factory):
    FACTORY_FOR = Key

    host = factory.SubFactory(HostFactory)
    key = factory.Sequence(lambda n: 'd0ntp4nic_{0}'.format(n))


class KeyRingFactory(factory.Factory):
    FACTORY_FOR = KeyRing

    user = factory.SubFactory(UserFactory)
    keys = factory.LazyAttribute(lambda a: [a._key1, a._key2, a._key3])

    _key1 = factory.SubFactory(KeyFactory)
    _key2 = factory.SubFactory(KeyFactory)
    _key3 = factory.SubFactory(KeyFactory)
