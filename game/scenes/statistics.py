from dataclasses import field, dataclass
from typing import List


@dataclass
class Statistics:
    cockroaches_on_map: int = 0
    food_on_map: int = 0
    spays_on_map: int = 0
    messages: List[str] = field(default_factory=list)

    def reset(self, cockroaches_on_map: int, food_on_map: int, spays_on_map: int):
        self.cockroaches_on_map = cockroaches_on_map
        self.food_on_map = food_on_map
        self.spays_on_map = spays_on_map
        self.messages = []

    def kill_cockroach(self):
        self.cockroaches_on_map -= 1
        self.messages.append("Cockroach is dead")

    def pick_food(self):
        self.food_on_map -= 1
        self.messages.append("Ate some food")

    def pick_spray(self):
        self.spays_on_map -= 1
        self.messages.append("Got a spray")

    def cockroach_ate_food(self):
        self.food_on_map -= 1
        self.cockroaches_on_map += 1

    def apply_spray(self):
        self.messages.append("Spray THEM!")
