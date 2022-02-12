import itertools
import random
from typing import Optional, Set, List

from core.geometry import Point, Delta, Rectangle
from game.map import Map
from game.nodes.game_nodes import Food, Spray, Cockroach, Player, Light, SprayZone
from game.scenes.base_scene import Scene
from game.scenes.statistics import Statistics


class MapScene(Scene):
    def __init__(
        self,
        frame: Rectangle,
        game_map: Map,
        player: Player,
        cockroaches: List[Cockroach],
        food: List[Food],
        sprays: List[Spray],
        field_of_view: int,
        statistics: Statistics
    ):
        super(MapScene, self).__init__(frame, [], [])
        self.game_map = game_map
        self.player = player
        self.field_of_view = field_of_view
        self.cockroaches = cockroaches
        self.food = food
        self.sprays = sprays
        self.statistics = statistics
        self.statistics.reset(len(cockroaches), len(food), len(sprays))
        self.update_state()

    def move_player(self, delta: Point):
        new_position = self.player.position + delta
        if not self.game_map.is_wall(new_position):
            self.player.move(delta)
            self.kill_cockroaches({new_position})
        food_piece = self.get_food(new_position)
        if food_piece:
            self.food.remove(food_piece)
            self.statistics.pick_food()
        spray = self.get_spray(new_position)
        if spray:
            self.sprays.remove(spray)
            self.player.pick_spray(spray)
            self.statistics.pick_spray()

        self.update_state()

    def apply_spray(self):
        spray = self.player.consume_spray()
        if spray is None:
            self.update_state()
        else:
            self.statistics.apply_spray()
            self.kill_cockroaches(self.killzone())
            self.update_state()
            for position in self.killzone():
                self.nodes.append(SprayZone(position))

    def update_state(self):
        self.nodes = []

        self.move_cockroaches()

        visible_positions = set(self.game_map.visible_positions(self.player.position, self.field_of_view))
        for visible_position in visible_positions:
            visible_tile = self.game_map.get_tile(visible_position)
            visible_tile.is_explored = True

        for tile in self.game_map.tiles():
            if tile.is_explored:
                self.nodes.append(tile)

        self.nodes.extend(food_pieces for food_pieces in self.food if food_pieces.position in visible_positions)
        self.nodes.extend(spray for spray in self.sprays if spray.position in visible_positions)
        self.nodes.extend(cockroach for cockroach in self.cockroaches if cockroach.position in visible_positions)
        self.nodes.append(self.player)
        for position in visible_positions:
            self.nodes.append(Light(position))

    def killzone(self) -> Set[Point]:
        return set(self.game_map.visible_positions(self.player.position, self.field_of_view // 2, False))

    def move_cockroaches(self):
        def empty_position_nearby(position: Point) -> Delta:
            variants = list(itertools.product([-1, 0, 1], repeat=2))
            random.shuffle(variants)
            for (x, y) in variants:
                if ((x, y) != (0, 0)
                        and not self.game_map.is_wall(position + Point(x, y))
                        and self.player.position != position + Point(x, y)):
                    return Point(x, y)
            return Point(0, 0)

        cockroach_children = []
        for cockroach in self.game_map.filter_visible_items(self.cockroaches, self.player.position, self.field_of_view):
            delta = empty_position_nearby(cockroach.position)
            cockroach.move(delta)
            food_piece = self.get_food(cockroach.position)
            if food_piece:
                self.food.remove(food_piece)
                cockroach.grow_up()
                cockroach_children.append(Cockroach(cockroach.position + empty_position_nearby(cockroach.position)))
                self.statistics.cockroach_ate_food()
        self.cockroaches.extend(cockroach_children)

    def kill_cockroaches(self, killzone: Set[Point]):
        for cockroach in self.cockroaches:
            if cockroach.position in killzone:
                if cockroach.is_huge:
                    cockroach.grow_down()
                else:
                    self.cockroaches.remove(cockroach)
                    self.statistics.kill_cockroach()

    def get_food(self, position: Point) -> Optional[Food]:
        for food_piece in self.food:
            if food_piece.position == position:
                return food_piece
        return None

    def get_spray(self, position: Point) -> Optional[Spray]:
        for aerosol in self.sprays:
            if aerosol.position == position:
                return aerosol
        return None
