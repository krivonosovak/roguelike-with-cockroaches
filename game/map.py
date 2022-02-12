from dataclasses import dataclass
from typing import List, Optional, Iterator

import numpy as np
import tcod

from core.geometry import Point
from game.nodes.base_node import Node
from game.nodes.game_nodes import TileNode, Ground, Wall


@dataclass
class Map:
    game_map: List[List[TileNode]]

    @property
    def width(self):
        return len(self.game_map)

    @property
    def height(self):
        if self.width != 0:
            return len(self.game_map[0])
        return 0

    def positions(self) -> Iterator[Point]:
        for x in range(self.width):
            for y in range(self.height):
                yield Point(x, y)

    def tiles(self) -> Iterator[TileNode]:
        for position in self.positions():
            yield self.get_tile(position)

    def visible_tiles(self, center: Point, radius: int, include_walls: bool = True):
        for position in self.visible_positions(center, radius, include_walls):
            yield self.get_tile(position)

    def visible_positions(self, center: Point, radius: int, include_walls: bool = True):
        mask = self.visibility_mask(center, radius, include_walls)
        for position in self.positions():
            if mask[position.x, position.y]:
                yield position

    def get_empty_tile_positions(self) -> List[Point]:
        empty_tiles_points = []
        for tile in self.tiles():
            if isinstance(tile, Ground):
                empty_tiles_points.append(tile.position)
        return empty_tiles_points

    def is_wall(self, position: Point):
        tile = self.get_tile(position)
        return isinstance(tile, Wall) or tile is None

    def get_tile(self, position: Point) -> Optional[TileNode]:
        if 0 <= position.x < self.width and 0 <= position.y < self.height:
            return self.game_map[position.x][position.y]
        return None

    def filter_visible_items(self, items: List[Node], center: Point, radius: int) -> Iterator:
        mask = self.visibility_mask(center, radius)
        for item in items:
            if mask[item.position.x, item.position.y]:
                yield item

    def visibility_mask(self, center: Point, radius: int, light_walls: bool = True) -> np.ndarray:
        surroundings = tcod.map.Map(width=self.width, height=self.height)
        surroundings.transparent[:] = True
        for position in self.positions():
            if self.is_wall(position):
                surroundings.transparent[position.y, position.x] = False
        surroundings.compute_fov(center.x, center.y, radius=radius, light_walls=light_walls)
        return surroundings.fov.T
