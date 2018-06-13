import abc

import aggregates as a
import entities as e


class Action(abc.ABC):

    @abc.abstractmethod
    def trigger(self): pass


class OpenDoorAction(Action):

    def __init__(self, door_name: str, doors_aggregate: a.Doors) -> None:
        self._door_name = door_name
        self._doors_aggregate = doors_aggregate

    def trigger(self):
        self._doors_aggregate.open(self._door_name)


class SpawnItemInInventoryAction(Action):

    def __init__(self, item: e.Item, inventory: a.PlayerInventory) -> None:
        self._item = item
        self._inventory = inventory

    def trigger(self):
        self._inventory.add_item_to_inventory(self._item)
