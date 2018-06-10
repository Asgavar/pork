from typing import Dict

from pork.actions import Action
import pork.events as e


class ItemUsedHandler:

    def __init__(self, item_used_mapping: Dict[str, Action]) -> None:
        self._item_used_mapping = item_used_mapping

    def __call__(self, event: e.ItemUsed):
        self._item_used_mapping[event.item_name].trigger()


class MonsterDiedHandler:

    def __init__(self, monster_died_mapping: Dict[str, Action]) -> None:
        self._monster_died_mapping = monster_died_mapping

    def __call__(self, event: e.MonsterDied):
        self._monster_died_mapping[event.monster_name].trigger()
