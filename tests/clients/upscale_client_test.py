import unittest
from unittest.mock import Mock, MagicMock

import requests

from src.clients.upscale_client import UpscaleClient

new_height = 200
new_width = 300
base64_image = 'encoded_image'

access_token = 'TEST_KEY'
request_url = "test.example"
request_string = '{"access_token": "TEST_KEY", "new_height": 200, "new_width": 300, "base64_image": "encoded_image"}'

upscaled_base64_image = 'upscaled_encoded_image'
response_body = {"base64_image": upscaled_base64_image}

class MyTestCase(unittest.TestCase):

    def test_successful_upscale(self):
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_response.json = MagicMock(return_value=response_body)

        mocked_session = requests.Session()
        mocked_session.post = MagicMock(return_value=mocked_response)

        upscale_client = UpscaleClient(request_url, access_token)
        upscale_client._session = mocked_session

        upscale_result = upscale_client.upscale(new_height, new_width, base64_image)

        self.assertEqual(upscale_result.base64_image, upscaled_base64_image)

    def test_non_200_response(self):
        mocked_response = Mock()
        mocked_response.status_code = 400

        mocked_session = requests.Session()
        mocked_session.post = MagicMock(return_value=mocked_response)

        upscale_client = UpscaleClient(request_url, access_token)
        upscale_client._session = mocked_session

        upscale_result = upscale_client.upscale(new_height, new_width, base64_image)

        self.assertEqual(upscale_result, None)


if __name__ == '__main__':
    unittest.main()
