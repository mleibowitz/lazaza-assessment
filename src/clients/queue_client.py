import abc
from pathlib import Path
import json
from collections import deque
import random


class AbstractQueueClient(abc.ABC):
    @abc.abstractmethod
    def pop(self) -> dict | None:
        pass


class QueueClient(AbstractQueueClient):
    def __init__(self) -> None:
        with open(Path('.').parent / "images.json", "r") as images_file:
            self._images: deque[str] = deque(json.load(images_file))


    def _random_number_divisible_by_100(self) -> int:
        start = 3
        end = 10
        divisible_by_100 = [num * 100 for num in range(start, end)]
        return random.choice(divisible_by_100)

    def _generate_message(self) -> dict:
        width = self._random_number_divisible_by_100()
        height = self._random_number_divisible_by_100()
        image_data = self._images if width > 400 else self._images[0]
        return {"width": width, "height": height, "image_data": image_data}

    def pop(self) -> dict | None:
        if len(self._images) == 0:
            return None

        return self._generate_message()
