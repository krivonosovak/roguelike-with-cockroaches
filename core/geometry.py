from dataclasses import dataclass
from math import sqrt
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def step_towards(self, target: "Point") -> "Delta":
        dx = target.x - self.x
        dy = target.y - self.y
        distance = sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return Point(dx, dy)

    def step_away_from(self, target: "Point") -> "Delta":
        return -self.step_towards(target)

    def distance_to(self, other: "Point") -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return sqrt(dx ** 2 + dy ** 2)


Delta = Point


@dataclass
class Rectangle:
    upper_left: Point
    width: int
    height: int

    @property
    def lower_right(self) -> Point:
        return Point(
            self.upper_left.x + self.width,
            self.upper_left.y + self.height
        )

    @property
    def center(self) -> Point:
        return Point(
            (self.upper_left.x + self.lower_right.x) // 2,
            (self.upper_left.y + self.lower_right.y) // 2
        )

    def intersected(self, other: "Rectangle") -> bool:
        return not (
                self.lower_right.x < other.upper_left.x
                or self.upper_left.x > other.lower_right.x
                or self.upper_left.y < other.lower_right.y
                or self.lower_right.y > other.upper_left.y
        )