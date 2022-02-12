import tcod

from core.color import Color
from core.geometry import Rectangle, Point
from game.nodes.game_nodes import Player
from game.nodes.ui_nodes import BoxNode, TextNode
from game.scenes.base_scene import Scene
from game.scenes.statistics import Statistics


class PanelScene(Scene):
    def __init__(self, frame: Rectangle, statistics: Statistics, player: Player):
        super(PanelScene, self).__init__(frame, [], [])
        self.statistics = statistics
        self.player = player

    def layout(self):
        self.nodes = []
        self.nodes.extend([
            # Inventory
            BoxNode(
                Rectangle(self.frame.upper_left + Point(2, 2), 11, self.frame.height - 3),
                Color.inventory_background
            ),
            TextNode(self.frame.upper_left + Point(3, 3), "Inventory", Color.header_color, tcod.LEFT),
            TextNode(self.frame.upper_left + Point(3, 5), f"Sprays: {len(self.player.sprays)}", Color.white, tcod.LEFT),

            # Statistics box
            BoxNode(
                Rectangle(self.frame.upper_left + Point(19, 2), 17, self.frame.height - 3),
                Color.inventory_background
            ),
            TextNode(self.frame.upper_left + Point(28, 3), "World info", Color.header_color, tcod.CENTER),
            TextNode(self.frame.upper_left + Point(20, 5), "Cockroches: ", Color.white, tcod.LEFT),
            TextNode(
                self.frame.upper_left + Point(20 + len("Cockroches: "), 5),
                f"{self.statistics.cockroaches_on_map}", Color.red, tcod.LEFT
            ),
            TextNode(
                self.frame.upper_left + Point(20, 6), f"Food: {self.statistics.food_on_map} ", Color.white, tcod.LEFT
            ),
            TextNode(
                self.frame.upper_left + Point(20, 7), f"Sprays: {self.statistics.spays_on_map} ", Color.white, tcod.LEFT
            )
        ])

        # Log box
        self.nodes.extend([
            BoxNode(
                Rectangle(self.frame.upper_left + Point(42, 2), 35, self.frame.height - 3),
                Color.inventory_background
            ),
            TextNode(self.frame.upper_left + Point(57, 3), "Events", Color.header_color, tcod.CENTER)
        ])
        messages_count = 5
        for i, message in enumerate(reversed(self.statistics.messages)):
            if i == messages_count:
                break
            self.nodes.append(TextNode(self.frame.upper_left + Point(43, 5 + i), message, Color.white, tcod.LEFT))
