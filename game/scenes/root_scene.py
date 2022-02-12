from core.geometry import Rectangle
from game.config import MapConfig
from game.scenes.game_scene import GameScene
from game.scenes.menu_scenes import MenuScene, WinMenuScene
from game.scenes.base_scene import Scene


def exit_game():
    raise SystemExit()


class RootScene(Scene):
    def __init__(self, frame: Rectangle, map_parameters: MapConfig):
        super(RootScene, self).__init__(frame, [], [])
        self.menu_scene = MenuScene(
            frame=frame,
            on_start_game=lambda: self.start_game(),
            on_exit=lambda: exit_game()
        )
        self.game_scene = GameScene(
            frame=frame,
            map_parameters=map_parameters,
            on_exit=lambda: self.open_menu(),
            game_win=lambda: self.open_win_menu()
        )
        self.win_menu = WinMenuScene(
            frame=frame,
            on_start_game=lambda: self.start_game(),
            on_exit=lambda: exit_game()
        )
        self.children = [self.menu_scene]

    def start_game(self):
        self.game_scene.restart_game()
        self.children = [self.game_scene]

    def open_menu(self):
        self.children = [self.menu_scene]

    def open_win_menu(self):
        self.children = [self.win_menu]

