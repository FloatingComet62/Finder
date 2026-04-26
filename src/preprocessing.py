"""
a. Input data preparation function
b. Feature Extraction
"""

from random import choices
from string import ascii_letters
from inference import models
from logger import ModuleLogger
from utils import Vector2
import math

logger = ModuleLogger("Preprocessing")

ITEM_INSERTION_DIFF = 10000
MAX_ITERATION_SIGNAL_STRENGTH = 20


class Item:
    def __init__(self, class_name, position, confidence):
        self.id = "".join(choices(ascii_letters, k=32))
        self.name = class_name
        self.position = position
        self.velocity = Vector2(0, 0)
        self.confidence = confidence
        self.signal_strength = int(MAX_ITERATION_SIGNAL_STRENGTH * confidence)

    def from_box(box, model):
        x1, y1, x2, y2 = box.xyxy[0]
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        return Item(
            model.names[int(box.cls)],
            Vector2(cx, cy),
            float(box.conf),
        )

    def __repr__(self):
        pos = repr(self.position)
        effective_confidence = self.effective_confidence()
        confidence_percent = round(effective_confidence * 100, 2)
        return f'Item(name="{self.name}", position={pos}, confidence={confidence_percent}%)'

    def compare(self, other):
        if self.name != other.name:
            return math.inf

        actual_velocity = (other.position - self.position).norm()
        velocity_disparity_dotproduct = (
            actual_velocity.x * self.velocity.x + actual_velocity.y * self.velocity.y
        )
        velocity_disparity = 6 / (velocity_disparity_dotproduct + 3) - 1

        diff = (other.position - self.position)**2
        return math.sqrt(diff.x + diff.y) * velocity_disparity

    def update(self, other):
        self.velocity = (other.position - self.position).norm()
        self.position = (
            self.position * self.confidence + other.position * other.confidence
        ) / (self.confidence + other.confidence)
        self.signal_strength += int(MAX_ITERATION_SIGNAL_STRENGTH * other.confidence)
        self.confidence = (self.confidence + other.confidence) / 2

    def tick(self) -> bool:
        self.signal_strength -= 1
        return self.signal_strength > 0

    def effective_confidence(self):
        effective_signal = self.signal_strength / MAX_ITERATION_SIGNAL_STRENGTH
        signal_coefficient = 0.5 * math.tanh(effective_signal / 3 - 2) + 0.5
        return signal_coefficient * self.confidence


class ItemTagger:
    def __init__(self):
        self.tagged_objects = []

    def add_from_results(self, models_results):
        logger.debug("Adding", sum(map(lambda x: len(x[0].boxes), models_results)), "results")
        for obj in self.tagged_objects:
            if obj.effective_confidence() < 0.1:
                continue
            logger.debug(obj)
        items = []
        for model_results in models_results:
            for i, result in enumerate(models_results):
                if len(result) == 0:
                    continue

                for box in result[0].boxes:
                    items.append(Item.from_box(box, models[i]))

        if len(self.tagged_objects) == 0:
            for item in items:
                self.tagged_objects.append(item)
            return

        for i in range(len(self.tagged_objects)):
            for item in items[:]:
                if self.tagged_objects[i].compare(item) > ITEM_INSERTION_DIFF:
                    continue

                self.tagged_objects[i].update(item)
                items.remove(item)
                break

        for item in items:
            self.tagged_objects.append(item)

        for tagged_object in self.tagged_objects:
            should_keep = tagged_object.tick()
            if should_keep:
                continue
            self.tagged_objects.remove(tagged_object)
