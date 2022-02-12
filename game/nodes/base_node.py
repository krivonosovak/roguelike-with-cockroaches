from abc import abstractmethod, ABC
from dataclasses import dataclass

from tcod import Console

from core.geometry import Point, Rectangle


@dataclass
class Node(ABC):
    frame: Rectangle

    @property
    def position(self):
        return self.frame.upper_left

    @position.setter
    def position(self, value: Point):
        self.frame.upper_left = value

    @abstractmethod
    def draw(self, console: Console):
        pass
