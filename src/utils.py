"""
a. Redundant functions
b. Helper functions
"""

import math


class Vector2:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def norm(self):
        dist = math.sqrt(self.x**2 + self.y**2)
        return Vector2(self.x / dist, self.y / dist)

    def __repr__(self):
        return f"Vector2({round(self.x, 2)}, {round(self.y, 2)})"

    def __add__(a, b):
        v = Vector2(0, 0)
        if isinstance(b, Vector2):
            v.x = a.x + b.x
            v.y = a.y + b.y
            return v

        if isinstance(b, (float, int)):
            v.x = a.x + b
            v.y = a.y + b
            return v

        raise Exception("Invalid Vector2 addition")

    def __sub__(a, b):
        v = Vector2(0, 0)
        if isinstance(b, Vector2):
            v.x = a.x - b.x
            v.y = a.y - b.y
            return v

        if isinstance(b, (float, int)):
            v.x = a.x - b
            v.y = a.y - b
            return v

        raise Exception("Invalid Vector2 subtraction")

    def __mul__(a, b):
        v = Vector2(0, 0)
        if isinstance(b, Vector2):
            v.x = a.x * b.x
            v.y = a.y * b.y
            return v

        if isinstance(b, (float, int)):
            v.x = a.x * b
            v.y = a.y * b
            return v

        raise Exception("Invalid Vector2 multiplication")

    def __truediv__(a, b):
        v = Vector2(0, 0)
        if isinstance(b, Vector2):
            v.x = a.x / b.x
            v.y = a.y / b.y
            return v

        if isinstance(b, (float, int)):
            v.x = a.x / b
            v.y = a.y / b
            return v

        raise Exception("Invalid Vector2 true division")

    def __floordiv__(a, b):
        v = Vector2(0, 0)
        if isinstance(b, Vector2):
            v.x = a.x // b.x
            v.y = a.y // b.y
            return v

        if isinstance(b, (float, int)):
            v.x = a.x // b
            v.y = a.y // b
            return v

        raise Exception("Invalid Vector2 floor division")

    def __pow__(a, b):
        v = Vector2(0, 0)
        if isinstance(b, Vector2):
            v.x = a.x**b.x
            v.y = a.y**b.y
            return v

        if isinstance(b, (float, int)):
            v.x = a.x**b
            v.y = a.y**b
            return v

        raise Exception("Invalid Vector2 power")
