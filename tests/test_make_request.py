import unittest
from outages import make_request
from unittest.mock import patch, MagicMock
import sys
import io

class TestMakeRequest(unittest.TestCase):
    """ This class contains tests for the make_request function
        in outages.py.
    """
    @patch('outages.requests')
    def test_status_code_200_get(self, mock_request):
        """ Given the server returns status code 200 after a GET request
            Then the make_request function returns the data
            And a '200 OK' message is printed
        """
        mock_response = MagicMock()
        mock_response.status_code = 200 # simulate 200 OK response
        mock_response.json.return_value = {
            'id': '123',
            'begin': '12:00',
            'end': '13:00'
        }
        mock_request.get.return_value = mock_response # mock request.get() returns response json
        capturedOutput = io.StringIO()  # create StringIO object to store stdout
        sys.stdout = capturedOutput  # direct output to new StringIO object
        self.assertEqual(make_request('GET', 'url', {'key': 'val'}), {'id': '123','begin': '12:00','end': '13:00'}) # capture output
        sys.stdout = sys.__stdout__
        self.assertEqual('200 OK\n', capturedOutput.getvalue())
    
    @patch('sys.exit')
    @patch('outages.requests')
    def test_status_code_200_get_none(self, mock_request, mock_exit):
        """ Given the server returns status code 200 after a GET request
            And returns an invalid payload (None)
            Then the make_request function calls sys.exit
            And prints an error message
        """
        mock_response = MagicMock()
        mock_response.status_code = 200 # simulate 200 OK response
        mock_response.json.return_value = None
        mock_request.get.return_value = mock_response # mock request.get() returns response json
        capturedOutput = io.StringIO()  # create StringIO object to store stdout
        sys.stdout = capturedOutput
        make_request('GET', 'url', {'key': 'val'}) # capture output
        sys.stdout = sys.__stdout__
        mock_exit.assert_called_once_with(1)
        self.assertTrue('200 OK' in capturedOutput.getvalue())
        self.assertTrue('Server returned 200 but no valid data' in capturedOutput.getvalue())
        
    @patch('outages.requests')
    def test_status_code_200_post(self, mock_request):
        """ Given the server returns status code 200 after a POST request
            Then the make_request function returns status code 200
            And a '200 OK' message is printed
        """
        mock_response = MagicMock()
        mock_response.status_code = 200 # simulate 200 OK response

        mock_request.post.return_value = mock_response # mock request.post() returns mock response
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.assertEqual(make_request('POST', 'url', {'key': 'val'}), 200)
        sys.stdout = sys.__stdout__
        self.assertEqual('200 OK\n', capturedOutput.getvalue())

    @patch('sys.exit')
    @patch('outages.requests')
    def test_status_code_client_error_403_get(self, mock_request, mock_exit):
        """ Given the server returns status code 403 after a GET request
            Then the make_request function exits the interpreter using sys.exit
            And a 'Error (403: Forbidden)' message is printed
        """
        mock_response = MagicMock()
        mock_response.status_code = 403 # simulate 403 forbidden response
        mock_request.get.return_value = mock_response

        capturedOutput = io.StringIO() # create StringIO object to store stdout
        sys.stdout = capturedOutput # direct output to new StringIO object
        make_request('GET', 'url', {'key': 'val'}) # capture output
        sys.stdout = sys.__stdout__ 

        mock_exit.assert_called_once_with(1)  # assert mock sys.exit was called 
        self.assertEqual('Error (403: Forbidden)\n', capturedOutput.getvalue()) # assert correct error message

    @patch('sys.exit')
    @patch('outages.requests')
    def test_status_code_client_error_403_post(self, mock_request, mock_exit):
        """ Given the server returns status code 403 after a POST request
            Then the make_request function exits the interpreter using sys.exit
            And a 'Error (403: Forbidden)' message is printed
        """
        mock_response = MagicMock()
        mock_response.status_code = 403 # simulate 403 forbidden response
        mock_request.post.return_value = mock_response

        capturedOutput = io.StringIO() # create StringIO object to store stdout
        sys.stdout = capturedOutput # direct output to new StringIO object
        make_request('POST', 'url', {'key': 'val'}) # capture output
        sys.stdout = sys.__stdout__ 

        mock_exit.assert_called_once_with(1)  # assert mock sys.exit was called 
        self.assertEqual('Error (403: Forbidden)\n', capturedOutput.getvalue()) # assert correct error message

    @patch('sys.exit')
    @patch('outages.requests')
    def test_status_code_client_error_404_get(self, mock_request, mock_exit):
        """ Given the server returns status code 404 after a GET request
            Then the make_request function exits the interpreter using sys.exit
            And a 'Error (404: Not Found)' message is printed
        """
        mock_response = MagicMock()
        mock_response.status_code = 404 # simulate 403 forbidden response
        mock_request.get.return_value = mock_response

        capturedOutput = io.StringIO() # create StringIO object to store stdout
        sys.stdout = capturedOutput # direct output to new StringIO object
        make_request('GET', 'url', {'key': 'val'}) # capture output
        sys.stdout = sys.__stdout__ 

        mock_exit.assert_called_once_with(1)  # assert mock sys.exit was called 
        self.assertEqual('Error (404: Not Found)\n', capturedOutput.getvalue()) # assert correct error message
    
    @patch('sys.exit')
    @patch('outages.requests')
    def test_status_code_client_error_404_post(self, mock_request, mock_exit):
        """ Given the server returns status code 404 after a POST request
            Then the make_request function exits the interpreter using sys.exit
            And a 'Error (404: Not Found)' message is printed
        """
        mock_response = MagicMock()
        mock_response.status_code = 404 # simulate 403 forbidden response
        mock_request.post.return_value = mock_response

        capturedOutput = io.StringIO() # create StringIO object to store stdout
        sys.stdout = capturedOutput # direct output to new StringIO object
        make_request('POST', 'url', {'key': 'val'}) # capture output
        sys.stdout = sys.__stdout__ 

        mock_exit.assert_called_once_with(1)  # assert mock sys.exit was called 
        self.assertEqual('Error (404: Not Found)\n', capturedOutput.getvalue()) # assert correct error message

    @patch('sys.exit')
    @patch('outages.requests')
    def test_status_code_client_error_429_get(self, mock_request, mock_exit):
        """ Given the server returns status code 429 after a GET request
            Then the make_request function exits the interpreter using sys.exit
            And a 'Error (429: Too Many Requests)' message is printed
        """
        mock_response = MagicMock()
        mock_response.status_code = 429 # too many requests
        mock_request.get.return_value = mock_response

        capturedOutput = io.StringIO() # create StringIO object to store stdout
        sys.stdout = capturedOutput # direct output to new StringIO object
        make_request('GET', 'url', {'key': 'val'}) # capture output
        sys.stdout = sys.__stdout__

        mock_exit.assert_called_once_with(1)  # assert mock sys.exit was called 
        self.assertEqual('Error (429: Too Many Requests)\n', capturedOutput.getvalue()) # assert correct error message
    
    @patch('sys.exit')
    @patch('outages.requests')
    def test_status_code_client_error_429_post(self, mock_request, mock_exit):
        """ Given the server returns status code 429 after a POST request
            Then the make_request function exits the interpreter using sys.exit
            And a 'Error (429: Too Many Requests)' message is printed
        """
        mock_response = MagicMock()
        mock_response.status_code = 429 # too many requests
        mock_request.post.return_value = mock_response

        capturedOutput = io.StringIO() # create StringIO object to store stdout
        sys.stdout = capturedOutput # direct output to new StringIO object
        make_request('POST', 'url', {'key': 'val'}) # capture output
        sys.stdout = sys.__stdout__

        mock_exit.assert_called_once_with(1)  # assert mock sys.exit was called 
        self.assertEqual('Error (429: Too Many Requests)\n', capturedOutput.getvalue()) # assert correct error message

    @patch('sys.exit')
    @patch('outages.requests')
    def test_status_code_server_error_500_get(self, mock_request, mock_exit):
        """ Given the server returns status code 500 after a GET request
            Then the make_request function exits the interpreter using sys.exit
            And a 'Retrying... 5/5' message is printed, indicating 5 retries
            And a 'Error (500: Internal Server Error)' message is printed
        """
        mock_response = MagicMock()
        mock_response.status_code = 500 # not found
        mock_request.get.return_value = mock_response

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        make_request('GET', 'url', {'key': 'val'})
        sys.stdout = sys.__stdout__

        mock_exit.assert_called_once_with(1) # assert mock sys.exit was called 
        self.assertTrue('Retrying... 5/5' in capturedOutput.getvalue()) # assert 5 retries have happened...
        self.assertTrue('Error (500: Internal Server Error)' in capturedOutput.getvalue()) # ...and the last one failed