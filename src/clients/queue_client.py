import abc
from pathlib import Path
import json
from collections import deque
import random


class AbstractQueueClient(abc.ABC):
    @abc.abstractmethod
    def pop(self) -> dict:
        pass


class QueueClient(AbstractQueueClient):
    def __init__(self) -> None:
        with open(Path(__file__).parent / "images.json", "r") as images_file:
            self._images: deque[str] = deque(json.load(images_file))

    def _random_number_divisible_by_100(start: int = 300, end: int = 1000) -> int:
        divisible_by_100 = [num * 100 for num in range(int(start / 100), int(end / 100) + 1)]
        return random.choice(divisible_by_100)

    def _generate_message(self) -> dict:
        width = height = self._random_number_divisible_by_100()
        image_data = self._images.pop() if width > 400 else self._images[0]
        return {"width": width, "height": height, "image_data": image_data}

    def pop(self) -> dict:
        return self._generate_message()
