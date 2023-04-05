import json
import unittest
from unittest.mock import MagicMock, patch
from io import StringIO

from src.app.app import app


class TestHandlePubsubMessage(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        self.test_cases = {}
        self.prep_tests()

    def tearDown(self):
        pass

    def prep_tests(self):
        tests = {}
        message = {'data': 'SGVsbG8gV29ybGQ='}  # 'Hello World'

        # Case 1: Happy case
        request = {'message': message}
        response = {'data': 'COMPLETED', 'status_code': 202}
        log = 'Pub/Sub message received: Hello World'
        tests['case 1'] = {'request': request, 'expected_response': response, 'log': log}

        # Case 2: No message
        request = {'messages': message}
        response = {'data': 'Bad Request: No message received', 'status_code': 400}
        tests['case 2'] = {'request': request, 'expected_response': response}

        # Case 3: No envelope
        request = ''
        response = {'data': 'Bad Request: No Pub/Sub message received', 'status_code': 400}
        tests['case 3'] = {'request': request, 'expected_response': response}

        self.test_cases['handle_pubsub_message'] = tests

    def run_test(self, key, test, mock_stdout, mock_hello_world):
        request = json.dumps(test['request'])
        expected_response = test['expected_response']
        response = self.app.post('/', data=request, content_type='application/json')
        
        self.assertEqual(expected_response['status_code'], response.status_code)
        self.assertEqual(expected_response['data'], response.data.decode('utf-8'))
        if 'log' in test:
            self.assertIn(test['log'], mock_stdout.getvalue().strip())
            mock_hello_world.assert_called_once()  # assert hello_world() function is called

    @patch('sys.stdout', new_callable=StringIO)
    @patch('src.app.app.hello_world')
    def test_handle_pubsub_message(self, mock_hello_world, mock_stdout):
        for key, test in self.test_cases['handle_pubsub_message'].items():
            self.run_test(key, test, mock_stdout, mock_hello_world)
        
        # TODO add test where the api path is wrong

    #def test_handle_errors(self):   

if __name__ == '__main__':
    unittest.main()
