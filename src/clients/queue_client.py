import abc
import os
import json
from collections import deque
import random
from pydantic import BaseModel


class QueueItem(BaseModel):
    width: int
    height: int
    image_data: str


class AbstractQueueClient(abc.ABC):
    @abc.abstractmethod
    def pop(self) -> dict | None:
        pass


class QueueClient(AbstractQueueClient):
    def __init__(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), 'images.json'), "r") as images_file:
            self._images: deque[str] = deque(json.load(images_file))

    def _random_number_divisible_by_100(self) -> int:
        start = 3
        end = 10
        divisible_by_100 = [num for num in range(start, end)]
        return 100 * random.choice(divisible_by_100)

    def _generate_message(self) -> QueueItem:
        width = self._random_number_divisible_by_100()
        height = self._random_number_divisible_by_100()
        image_data = self._images.pop() if (width > 400 and height > 400) else self._images[0]
        return QueueItem(width=width,
                         height=height,
                         image_data=image_data)

    def pop(self) -> QueueItem | None:
        if len(self._images) == 0:
            return None

        return self._generate_message()
