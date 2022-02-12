from asyncio import Event

import tcod

from core.color import Color
from core.geometry import Rectangle, Point
from game.nodes.ui_nodes import TextNode, BoxNode
from game.scenes.base_scene import Scene, Callback


class MenuScene(Scene):

    def __init__(self, frame: Rectangle, on_start_game: Callback, on_exit: Callback):
        super(MenuScene, self).__init__(frame, [], [])
        self.on_start_game = on_start_game
        self.on_exit = on_exit
        self.nodes = [
            TextNode(Point(frame.width // 2, frame.height // 2 - 10), "KILL COCKROACHES", Color.red),
            TextNode(Point(frame.width // 2, frame.height // 2 - 6), "Press [Enter] to kill ", Color.white),
            TextNode(Point(frame.width // 2, frame.height // 2 - 4), "Press [Esc] to give up", Color.white),
            BoxNode(Rectangle(Point(frame.width // 2 - 11, frame.height // 2), 22, 11), Color.panel_box, False),
            TextNode(Point(frame.width // 2 - 8, frame.height // 2 + 2), "Use", Color.white),
            TextNode(Point(frame.width // 2 - 2, frame.height // 2 + 2), "← ↑ ↓ →", Color.header_color),
            TextNode(Point(frame.width // 2 + 6, frame.height // 2 + 2), "to move", Color.white),
            TextNode(Point(frame.width // 2 - 5, frame.height // 2 + 4), "Use", Color.white),
            TextNode(Point(frame.width // 2 - 2, frame.height // 2 + 4), "S", Color.header_color),
            TextNode(Point(frame.width // 2 + 4, frame.height // 2 + 4), "to spray", Color.white),
            TextNode(Point(frame.width // 2, frame.height // 2 + 6), "Kill cockroaches", Color.white),
            TextNode(Point(frame.width // 2, frame.height // 2 + 7), "and", Color.white),
            TextNode(Point(frame.width // 2, frame.height // 2 + 8), "Don't let them eat", Color.white)
        ]

    def handle(self, event: Event) -> bool:
        if isinstance(event, tcod.event.KeyDown):
            if event.sym == tcod.event.K_RETURN:
                self.on_start_game()
                return True
            if event.sym == tcod.event.K_ESCAPE:
                self.on_exit()
                return True
        return False


class WinMenuScene(Scene):

    def __init__(self, frame: Rectangle, on_start_game: Callback, on_exit: Callback):
        super(WinMenuScene, self).__init__(frame, [], [])
        self.on_start_game = on_start_game
        self.on_exit = on_exit
        self.nodes = [
            TextNode(Point(frame.width // 2, frame.height // 2 - 3), "YOU KILLED THEM ALL", Color.red),
            TextNode(Point(frame.width // 2, frame.height // 2), "Press [Enter] to start again", Color.white),
            TextNode(Point(frame.width // 2, frame.height // 2 + 2), "Press [Esc] to exit", Color.white)
        ]

    def handle(self, event: Event) -> bool:
        if isinstance(event, tcod.event.KeyDown):
            if event.sym == tcod.event.K_RETURN:
                self.on_start_game()
                return True
            if event.sym == tcod.event.K_ESCAPE:
                self.on_exit()
                return True
        return False
