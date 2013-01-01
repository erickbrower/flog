import factory
from woodhouse.models import Application, Log

class ApplicationFactory(factory.Factory):
    FACTORY_FOR = Application

    name = factory.Sequence(lambda n: 'Test Application {0}'.format(n))
    instance = 'test'
    api_key = factory.Sequence(lambda n: 'key_{0}'.format(n))
    api_private_key = factory.Sequence(lambda n: 'private_key_{0}'.format(n))
    description = 'This is a test description!'


class LogFactory(factory.Factory):
    FACTORY_FOR = Log

    content = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    application = factory.SubFactory(ApplicationFactory)
