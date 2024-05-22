import abc
from pydantic import BaseModel
import json


class ImageServiceResponse(BaseModel):
    status_code: int
    body: str

    def json(self) -> dict:
        return json.loads(self.body)
    

class AbstractImageServiceClient(abc.ABC):
    @abc.abstractmethod
    def post_image(self, image: bytes) -> ImageServiceResponse:
        pass


class ImageServiceClient(AbstractImageServiceClient):
    def post_image(self, image: bytes) -> ImageServiceResponse:
        # This is a simple implementation that always returns success
        return ImageServiceResponse(status_code=200, body=json.dumps({"message": "Image uploaded successfully"}))
