import abc
from pydantic import BaseModel
import json
import requests
from requests.adapters import HTTPAdapter, Retry
import logging

logger = logging.getLogger(__name__)


class UpscalingServiceResponse(BaseModel):
    base64_image: str


class AbstractUpscaleClient(abc.ABC):
    @abc.abstractmethod
    def upscale(self, new_height, new_width, image_data) -> dict:
        pass


class UpscaleClient(AbstractUpscaleClient):
    def __init__(self, upscale_service_url, upscale_service_api_key):
        self._upscale_service_url = upscale_service_url
        self._upscale_service_api_key = upscale_service_api_key

        self._session = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500],
                        allowed_methods=['POST'])
        self._session.mount(self._upscale_service_url, HTTPAdapter(max_retries=retries))

    def upscale(self, new_height, new_width, image_data) -> UpscalingServiceResponse | None:
        request_body = {
            'access_token': self._upscale_service_api_key,
            'new_height': new_height,
            'new_width': new_width,
            'base64_image': image_data,
        }

        response = self._session.post(self._upscale_service_url, data=json.dumps(request_body))

        if response.status_code == 200:
            return UpscalingServiceResponse(**response.json())

        logger.error('Encountered error while upscaling image. {}: {} {}; Request: {},{}'.format(
            response.status_code,
            response.reason,
            response.json(),
            request_body['new_width'],
            request_body['new_height']))

        return None
