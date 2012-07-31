import os
from woodhouse import app
from woodhouse.models import Application, Log
import unittest


class WoodhouseTestCase(unittest.TestCase):

    def setUp(self):
        # app.config['MONGODB_DB'] = 'woodhouse_test'
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        Application.drop_collection()
        Log.drop_collection()

    def test_model_application(self):
        application = Application(
            name = 'HORY SHET IT\'S GOJIRA', 
            instance = 'DEV', 
            description = 'ARE JOO KEEDING?! RUN LIKE DE WEEND',
            api_key = 'HORY_SHET_GOJIRA',
            api_private_key = '12345678'
            )
        assert application.save()
        retrieved_app = Application.objects(api_key='HORY_SHET_GOJIRA').only('api_private_key')
        assert retrieved_app.count() == 1
        print retrieved_app.first().api_private_key
        log = Log(application=application, content={'GET': 'TO', 'THE': 'CHOPPA'})
        assert log.save()

        # application.delete()
        # retrieved_app = Application.objects(instance_name='DEV: HORY SHET IT\'S GOJIRA')
        # assert retrieved_app.count() == 0




if __name__ == '__main__':
    unittest.main()