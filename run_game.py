#!/usr/bin/env python3
import argparse
from pathlib import Path

import tcod

from core.color import Color
from core.geometry import Rectangle, Point
from game.config import Config, MapConfig
from game.scenes.root_scene import RootScene


def main(config_file: Path, map_config_file: Path):
    parameters = Config.from_json(config_file)
    map_parameters = MapConfig.from_json(map_config_file)
    tileset = tcod.tileset.load_tilesheet(parameters.path_to_fonts, 32, 8, tcod.tileset.CHARMAP_TCOD)
    with tcod.context.new(
            columns=parameters.screen_width,
            rows=parameters.screen_height,
            tileset=tileset,
            title="Kill cockroach",
            vsync=True,
    ) as context:
        root_console = tcod.Console(parameters.screen_width, parameters.screen_height, order="F")
        root_scene = RootScene(Rectangle(Point(0, 0), root_console.width, root_console.height), map_parameters)
        while True:
            root_console.clear(bg=Color.black.value)
            root_scene.draw(root_console)
            context.present(root_console)

            for event in tcod.event.wait():
                context.convert_event(event)
                root_scene.handle(event)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", type=Path, default=Path("supplementary_materials/general_config.json"),
                        help="Path to config with game parameters"),
    parser.add_argument("--map-config-file", type=Path, default=Path("supplementary_materials/map_config.json"),
                        help="Path to config with game parameters")

    args = parser.parse_args()
    main(**vars(args))
