import random
from dataclasses import dataclass
from random import randint
from typing import List, Callable

from core.geometry import Point, Rectangle
from game.map import Map
from game.nodes.game_nodes import TileNode, Wall, Cockroach, Spray, Food, Player, Ground


@dataclass
class GameGenerator:
    map_height: int
    map_width: int
    max_room_count: int
    min_room_count: int
    max_room_size: int
    min_room_size: int

    def generate_map(self) -> Map:

        game_map = self.__generate_map()
        return Map(game_map)

    def __generate_map(self) -> List[List[TileNode]]:
        game_map = [[Wall(Point(x, y)) for y in range(self.map_height)] for x in range(self.map_width)]
        all_rooms = []
        room_count = randint(self.min_room_count, self.max_room_count)
        for _ in range(room_count):
            room_width = randint(self.min_room_size, self.max_room_size)
            room_height = randint(self.min_room_size, self.max_room_size)
            x = randint(0, self.map_width - room_width - 1)
            y = randint(0, self.map_height - room_height - 1)
            room = Rectangle(Point(x, y), room_width, room_height)
            game_map = self.__add_room_to_map(room, game_map)
            if any(room.intersected(other_room) for other_room in all_rooms):
                all_rooms.append(room)
                continue
            if all_rooms:
                game_map = self.__add_vertical_tunnel(all_rooms[-1], room, game_map)
                game_map = self.__add_horizontal_tunnel(room, all_rooms[-1], game_map)
            all_rooms.append(room)

        return game_map

    @staticmethod
    def generate_cockroaches(game_map: Map, is_occupied: Callable[[Point], bool]) -> List[Cockroach]:
        cockroaches = []
        empty_tile_positions = game_map.get_empty_tile_positions()
        cockroach_count = randint(len(empty_tile_positions) // 20, len(empty_tile_positions) // 10)
        random.shuffle(empty_tile_positions)
        for position in empty_tile_positions:
            if len(cockroaches) == cockroach_count:
                break
            if is_occupied(position):
                continue
            cockroaches.append(Cockroach(position))
        return cockroaches

    @staticmethod
    def generate_sprays(game_map: Map, is_occupied: Callable[[Point], bool]) -> List[Spray]:
        sprays = []
        empty_tile_positions = game_map.get_empty_tile_positions()
        spray_count = randint(13, 20)
        random.shuffle(empty_tile_positions)
        for position in empty_tile_positions:
            if len(sprays) == spray_count:
                break
            if is_occupied(position):
                continue
            sprays.append(Spray(position))
        return sprays

    @staticmethod
    def generate_food(game_map: Map, is_occupied: Callable[[Point], bool]) -> List[Food]:
        food = []
        empty_tile_positions = game_map.get_empty_tile_positions()
        food_pieces_count = randint(20, 40)
        random.shuffle(empty_tile_positions)
        for position in empty_tile_positions:
            if len(food) == food_pieces_count:
                break
            if is_occupied(position):
                continue
            food.append(Food(position))
        return food

    @staticmethod
    def generate_player(game_map: Map) -> Player:
        empty_tile_positions = game_map.get_empty_tile_positions()
        random.shuffle(empty_tile_positions)
        return Player(empty_tile_positions[0])

    @staticmethod
    def __add_room_to_map(room: Rectangle, my_map: List[List[TileNode]]) -> List[List[TileNode]]:
        for x in range(room.upper_left.x, room.lower_right.x + 1):
            for y in range(room.upper_left.y, room.lower_right.y + 1):
                my_map[x][y] = Ground(Point(x, y))
        return my_map

    @staticmethod
    def __add_vertical_tunnel(
        room: Rectangle,
        other_room: Rectangle,
        my_map: List[List[TileNode]]
    ) -> List[List[TileNode]]:
        room_center = room.center
        other_room_center = other_room.center
        for y in range(min(room_center.y, other_room_center.y), max(room_center.y, other_room_center.y) + 1):
            my_map[room_center.x][y] = Ground(Point(room_center.x, y))
        return my_map

    @staticmethod
    def __add_horizontal_tunnel(
        room: Rectangle,
        other_room: Rectangle,
        my_map: List[List[TileNode]]
    ) -> List[List[TileNode]]:
        room_center = room.center
        other_room_center = other_room.center
        for x in range(min(room_center.x, other_room_center.x), max(room_center.x, other_room_center.x) + 1):
            my_map[x][room_center.y] = Ground(Point(x, room_center.y))
        return my_map
