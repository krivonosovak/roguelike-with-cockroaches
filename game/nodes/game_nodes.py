from dataclasses import dataclass
from typing import Optional

import tcod
from tcod import Console

from core.color import Color
from core.geometry import Point, Rectangle, Delta
from game.nodes.base_node import Node


@dataclass
class PointNode(Node):
    def __init__(self, position: Point, char: str, color: Color):
        super(PointNode, self).__init__(Rectangle(position, 1, 1))
        self.char = char
        self.color = color

    def move(self, delta: Delta):
        self.position += delta

    def draw(self, console: Console):
        console.print(x=self.position.x, y=self.position.y, string=self.char, fg=self.color.value)


@dataclass
class TileNode(Node):
    def __init__(self, position: Point, color: Color):
        super(TileNode, self).__init__(Rectangle(position, 1, 1))
        self.color = color
        self.is_explored = False

    def draw(self, console: Console):
        console.draw_rect(x=self.position.x, y=self.position.y, ch=0, height=1, width=1, bg=self.color.value)


@dataclass
class EffectNode(Node):
    def __init__(self, position: Point, color: Color):
        super(EffectNode, self).__init__(Rectangle(position, 1, 1))
        self.color = color

    def draw(self, console: Console):
        console.draw_rect(
            x=self.position.x,
            y=self.position.y,
            ch=0,
            height=1,
            width=1,
            bg=self.color.value,
            bg_blend=tcod.BKGND_ALPHA(200)
        )


class Wall(TileNode):
    def __init__(self, position: Point):
        super(Wall, self).__init__(position, Color.wall)


class Ground(TileNode):
    def __init__(self, position: Point):
        super(Ground, self).__init__(position, Color.ground)


class Spray(PointNode):
    def __init__(self, position: Point):
        super(Spray, self).__init__(position, "S", Color.blue)


class Player(PointNode):
    def __init__(self, position: Point):
        super().__init__(position, "@", Color.white)
        self.sprays = []

    def pick_spray(self, spray: Spray):
        print("dssd")
        self.sprays.append(spray)
        print(len(self.sprays))

    def consume_spray(self) -> Optional[Spray]:
        return self.sprays.pop() if self.sprays else None


class Food(PointNode):
    def __init__(self, position: Point):
        super(Food, self).__init__(position, "f", Color.green)


class Cockroach(PointNode):
    def __init__(self, position: Point, is_huge: bool = False):
        self.char = "C" if is_huge else "c"
        super(Cockroach, self).__init__(position, self.char, Color.red)
        self.is_huge = is_huge

    def grow_up(self):
        self.char = "C"
        self.is_huge = True

    def grow_down(self):
        self.char = "c"
        self.is_huge = False


class Light(EffectNode):
    def __init__(self, position: Point):
        super(Light, self).__init__(position, Color.light)


class SprayZone(EffectNode):
    def __init__(self, position: Point):
        super(SprayZone, self).__init__(position, Color.spray)
