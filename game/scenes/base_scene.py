from dataclasses import dataclass
from typing import Callable, List

from tcod import Console
from tcod.event import Event

from core.geometry import Rectangle
from game.nodes.base_node import Node

Callback = Callable[[], None]


@dataclass
class Scene:
    frame: Rectangle
    nodes: List[Node]
    children: List["Scene"]

    def handle(self, event: Event) -> bool:
        for child in reversed(self.children):
            if child.handle(event):
                return True
        return False

    def layout(self):
        pass

    def draw(self, console: Console):
        self.layout()
        for node in self.nodes:
            node.draw(console)
        for child in self.children:
            child.draw(console)
