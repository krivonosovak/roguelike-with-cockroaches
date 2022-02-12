from dataclasses import dataclass

import tcod
from tcod import Console

from core.color import Color
from core.geometry import Point, Rectangle
from game.nodes.base_node import Node


class TextNode(Node):
    def __init__(self, position: Point, text: str, color: Color, alignment: int = tcod.CENTER):
        super(TextNode, self).__init__(Rectangle(position, 0, 0))
        self.text = text
        self.color = color
        self.alignment = alignment

    def draw(self, console: Console):
        console.print(
            x=self.position.x,
            y=self.position.y,
            string=self.text,
            fg=self.color.value,
            alignment=self.alignment
        )


@dataclass
class BoxNode(Node):
    def __init__(self, frame: Rectangle, color: Color, is_filled=True):
        super(BoxNode, self).__init__(frame)
        self.color = color
        self.is_filled = is_filled

    def draw(self, console: Console):
        console.draw_frame(
            x=self.position.x,
            y=self.position.y,
            width=self.frame.width,
            height=self.frame.height,
            fg=self.color.value,
            bg=self.color.value if self.is_filled else None
        )
