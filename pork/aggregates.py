from collections import defaultdict
import functools
from typing import DefaultDict, Dict, List, Tuple

from pork.entities import Door, Item, Monster, WorldObject


class WorldLayout:
    HORIZONTAL_POSITION = 0
    VERTICAL_POSITION = 1

    def __init__(self, initial_horizontal: int=0, initial_vertical: int=0,
                 world_map: DefaultDict[Tuple, List[WorldObject]] =
                 defaultdict(lambda: [])) -> None:
        self._player_loc = [initial_horizontal, initial_vertical]
        self._world_map = world_map

    def _only_go_if_path_not_blocked(direction: str):  # type: ignore
        def real_decorator(func):
            @functools.wraps(func)
            def decorated(*args, **kwargs):
                if any(hasattr(worlditem, 'door_direction') and
                       worlditem.door_direction == direction and
                       worlditem.is_open is False
                       for worlditem in args[0].objects_in_the_current_room()):
                    pass
                else:
                    func(*args, **kwargs)
            return decorated
        return real_decorator

    @_only_go_if_path_not_blocked('north')
    def move_player_north(self) -> None:
        self._player_loc[self.VERTICAL_POSITION] += 1

    @_only_go_if_path_not_blocked('east')
    def move_player_east(self) -> None:
        self._player_loc[self.HORIZONTAL_POSITION] += 1

    @_only_go_if_path_not_blocked('south')
    def move_player_south(self) -> None:
        self._player_loc[self.VERTICAL_POSITION] -= 1

    @_only_go_if_path_not_blocked('west')
    def move_player_west(self) -> None:
        self._player_loc[self.HORIZONTAL_POSITION] -= 1

    def objects_in_the_current_room(self) -> List:
        return self._world_map[tuple(self._player_loc)]


class Doors:

    def __init__(self, doors_lookup: Dict[str, Door]={}) -> None:
        self._doors_lookup = doors_lookup

    def open(self, door_name: str):
        self._doors_lookup[door_name].is_open = True

    def close(self, door_name: str):
        self._doors_lookup[door_name].is_open = False

    def is_door_open(self, door_name: str) -> bool:
        return self._doors_lookup[door_name].is_open


class Monsters:

    def __init__(self, monsters: Dict[str, Monster]={}) -> None:
        self._monsters = monsters

    def attack(self, monster_name: str, power: int) -> None:
        self._monsters[monster_name].health -= power

    def is_monster_dead(self, monster_name: str) -> bool:
        return self._monsters[monster_name].health <= 0


class PlayerInventory:

    def __init__(self, player_items: List[Item]=[]) -> None:
        self._player_items = player_items

    def add_item_to_inventory(self, new_item: Item):
        self._player_items.append(new_item)

    def drop_item_from_inventory(self, item_to_drop: Item):
        self._player_items.remove(item_to_drop)

    def currently_held_items(self):
        return self._player_items
