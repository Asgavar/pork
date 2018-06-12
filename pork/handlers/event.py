from typing import Dict

from pork.actions import Action
from pork.aggregates import Monsters
import pork.events as e


class ItemUsedHandler:

    def __init__(self, item_used_mapping: Dict[str, Action]) -> None:
        self._item_used_mapping = item_used_mapping

    def __call__(self, event: e.ItemUsed):
        self._item_used_mapping[event.item_name].trigger()


class MonsterDiedHandler:

    def __init__(self, monsters: Monsters) -> None:
        self.monsters = monsters

    def __call__(self, event: e.MonsterDied):
        self.monsters.monster_action_mapping[event.monster_name].trigger()
