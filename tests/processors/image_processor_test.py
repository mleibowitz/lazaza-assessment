import unittest
from unittest.mock import MagicMock, Mock, call

from src.clients.image_service_client import ImageServiceClient, ImageServiceResponse
from src.clients.queue_client import QueueClient, QueueItem
from src.clients.upscale_client import UpscaleClient, UpscalingServiceResponse
from src.processors.image_processor import ImageProcessor

image_data = "<IMAGE>"
bad_image_data = "<BAD_IMAGE>"

queue_item_success = QueueItem(width=100, height=200, image_data=image_data)
queue_item_failure = QueueItem(width=400, height=300, image_data=image_data)

upscaled_image_data = "<UPSCALED_IMAGE>"
upscale_image_bytes = upscaled_image_data.encode('ascii')

image_service_response_success = ImageServiceResponse(status_code=200, body='')
image_service_response_failure = ImageServiceResponse(status_code=500, body='')


def upscale_returns(input_height, input_width, input_image_data):
    if input_image_data == image_data:
        return UpscalingServiceResponse(base64_image=upscaled_image_data)
    return None


class MyTestCase(unittest.TestCase):
    def test_empty_queue(self):
        mocked_queue_client = QueueClient()
        mocked_queue_client.pop = MagicMock(return_value=None)
        mocked_upscale_client = Mock()
        mocked_image_service_client = Mock()

        image_processor = ImageProcessor(mocked_queue_client, mocked_upscale_client, mocked_image_service_client)

        process_results = image_processor.process_queue()

        self.assertEqual(process_results.num_success, 0)
        self.assertEqual(process_results.num_failure, 0)

    def test_successful_queue(self):
        mocked_queue_client = QueueClient()
        mocked_queue_client.pop = Mock(side_effect=[queue_item_success, queue_item_success, queue_item_success, None])
        mocked_upscale_client = UpscaleClient('', '')
        mocked_upscale_client.upscale = MagicMock(side_effect=upscale_returns)
        mocked_image_service_client = ImageServiceClient()
        mocked_image_service_client.post_image = MagicMock(return_value=image_service_response_success)

        image_processor = ImageProcessor(mocked_queue_client, mocked_upscale_client, mocked_image_service_client)

        process_results = image_processor.process_queue()

        self.assertEqual(process_results.num_success, 3)
        self.assertEqual(process_results.num_failure, 0)

        mocked_upscale_client.upscale.assert_has_calls(
            [call(200, 100, image_data),
             call(200, 100, image_data),
             call(200, 100, image_data)])

        mocked_image_service_client.post_image.assert_has_calls(
            [call(upscale_image_bytes),
             call(upscale_image_bytes),
             call(upscale_image_bytes)]
        )


if __name__ == '__main__':
    unittest.main()
