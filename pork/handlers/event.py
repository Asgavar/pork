from aggregates import Monsters, PlayerInventory
import events as e


class ItemUsedHandler:

    def __init__(self, inventory: PlayerInventory) -> None:
        self.inventory = inventory

    def __call__(self, event: e.ItemUsed):
        self.inventory.item_action_mapping[event.item_name].trigger()


class MonsterDiedHandler:

    def __init__(self, monsters: Monsters) -> None:
        self.monsters = monsters

    def __call__(self, event: e.MonsterDied):
        if event.monster_name in self.monsters.monster_action_mapping:
            self.monsters.monster_action_mapping[event.monster_name].trigger()
        self.monsters._monsters.pop(event.monster_name)
