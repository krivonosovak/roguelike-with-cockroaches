import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    screen_width: int
    screen_height: int
    path_to_fonts: str

    @staticmethod
    def from_json(file: Path) -> "Config":
        with open(file) as in_json:
            parameters_dict = json.load(in_json)
        return Config(**parameters_dict)


@dataclass
class MapConfig:
    max_room_count: int
    min_room_count: int
    max_room_size: int
    min_room_size: int

    @staticmethod
    def from_json(file: Path) -> "MapConfig":
        with open(file) as in_json:
            parameters_dict = json.load(in_json)
        return MapConfig(**parameters_dict)
