from random import randint

import tcod
from tcod.event import Event

from core.geometry import Rectangle, Point
from game.config import MapConfig
from game.game_generator import GameGenerator
from game.map import Map
from game.scenes.base_scene import Scene, Callback
from game.scenes.map_scene import MapScene
from game.scenes.panel_scene import PanelScene
from game.scenes.statistics import Statistics


class GameScene(Scene):
    def __init__(self, frame: Rectangle, map_parameters: MapConfig, on_exit: Callback, game_win: Callback):
        super(GameScene, self).__init__(frame, [], [])
        self.parameters = map_parameters
        self.generator = GameGenerator(
            map_height=frame.height - 12,
            map_width=frame.width,
            min_room_count=map_parameters.min_room_count,
            max_room_size=map_parameters.max_room_size,
            min_room_size=map_parameters.min_room_size,
            max_room_count=map_parameters.max_room_count
        )
        self.on_exit = on_exit
        self.game_win = game_win

    def regenerate_game(self):
        self.statistics = Statistics()
        game_map = self.generator.generate_map()
        self.player = self.generator.generate_player(game_map)
        cockroaches = self.generator.generate_cockroaches(game_map, lambda p: False)

        def is_occupied_by_cockroach(point: Point) -> bool:
            return any(cockroach.position == point for cockroach in cockroaches)

        food = self.generator.generate_food(game_map, is_occupied_by_cockroach)

        def is_occupied_by_food(point: Point) -> bool:
            return any(food_piece.position == point for food_piece in food)

        sprays = self.generator.generate_sprays(
            game_map, lambda p: is_occupied_by_cockroach(p) or is_occupied_by_food(p)
        )
        self.map_scene = MapScene(
            frame=Rectangle(self.frame.upper_left, self.generator.map_width, self.generator.map_height),
            game_map=game_map,
            player=self.player,
            cockroaches=cockroaches,
            food=food,
            sprays=sprays,
            field_of_view=4,
            statistics=self.statistics
        )
        self.panel = PanelScene(
            frame=Rectangle(Point(0, self.map_scene.frame.height), self.frame.width, 12),
            statistics=self.statistics,
            player=self.player
        )

    def handle(self, event: Event) -> bool:
        result = False
        if isinstance(event, tcod.event.KeyDown):
            if event.sym == tcod.event.K_UP:
                self.map_scene.move_player(Point(0, -1))
                result = True
            elif event.sym == tcod.event.K_DOWN:
                self.map_scene.move_player(Point(0, 1))
                result = True
            elif event.sym == tcod.event.K_LEFT:
                self.map_scene.move_player(Point(-1, 0))
                result = True
            elif event.sym == tcod.event.K_RIGHT:
                self.map_scene.move_player(Point(1, 0))
                result = True
            elif event.sym == tcod.event.K_s:
                self.map_scene.apply_spray()
                result = True
            elif event.sym == tcod.event.K_ESCAPE:
                self.on_exit()
                return True

            if result and self.statistics.cockroaches_on_map == 0:
                self.game_win()

        return result

    @staticmethod
    def generate_player_position(game_map: Map) -> Point:
        possible_points_for_player = game_map.get_empty_tile_positions()
        point_index = randint(0, len(possible_points_for_player))
        return possible_points_for_player[point_index]

    def restart_game(self):
        self.regenerate_game()
        self.children = [self.map_scene, self.panel]
