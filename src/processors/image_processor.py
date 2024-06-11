import abc
from pydantic import BaseModel
from src.clients.image_service_client import ImageServiceClient
from src.clients.queue_client import QueueClient
from src.clients.upscale_client import UpscaleClient

import logging

logger = logging.getLogger(__name__)


class ProcessResults(BaseModel):
    num_success: int
    num_failure: int


def _convert_base64_image_to_bytes(base64_image: str) -> bytes:
    return base64_image.encode('ascii')  # TODO: ensure this is the correct encoding for the image service


class AbstractImageProcessor(abc.ABC):
    @abc.abstractmethod
    def process_queue(self) -> ProcessResults:
        pass


class ImageProcessor(AbstractImageProcessor):
    def __init__(self,
                 queue_client: QueueClient,
                 upscale_client: UpscaleClient,
                 image_service_client: ImageServiceClient):
        self._queue_client = queue_client
        self._upscale_client = upscale_client
        self._image_service_client = image_service_client

    def process_queue(self) -> ProcessResults:
        num_success = 0
        num_failure = 0

        queue_item = self._queue_client.pop()
        while queue_item:
            upscale_result = self._upscale_client.upscale(queue_item.height, queue_item.width, queue_item.image_data)
            if not upscale_result:
                num_failure += 1
            else:
                image_bytes = _convert_base64_image_to_bytes(upscale_result.base64_image)
                result = self._image_service_client.post_image(image_bytes)
                if result.status_code == 200:
                    num_success += 1
                else:
                    num_failure += 1
                    logger.error('Error uploading to image service: {}: {}'.format(
                        result.status_code, result.body))

            queue_item = self._queue_client.pop()

        return ProcessResults(num_success=num_success, num_failure=num_failure)
