from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple

from pork.entities import WorldObject, Item


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
            def decorated(*args, **kwargs):
                if any(hasattr(worlditem, 'door_direction') and
                       worlditem.door_direction == direction
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
        self._player_loc[self.HORIZONTAL_POSITION] -= 1

    @_only_go_if_path_not_blocked('west')
    def move_player_west(self) -> None:
        self._player_loc[self.VERTICAL_POSITION] -= 1

    def objects_in_the_current_room(self) -> List:
        return self._world_map[tuple(self._player_loc)]


class Doors:

    def __init__(self, doors_state: Dict[str, bool]={}) -> None:
        self._doors_state = doors_state

    def open(self, door_name: str):
        self._doors_state[door_name] = True

    def close(self, door_name: str):
        self._doors_state[door_name] = False

    def is_door_open(self, door_name: str) -> bool:
        return self._doors_state[door_name]


class Monsters:

    def __init__(self, monsters_health: Dict[str, int]={}) -> None:
        self._monsters_health = monsters_health

    def attack(self, monster_name: str, power: int) -> None:
        self._monsters_health[monster_name] -= power

    def is_monster_alive(self, monster_name: str) -> bool:
        return self._monsters_health[monster_name] > 0


class PlayerInventory:

    def __init__(self, player_items: List[Item]=[]) -> None:
        self._player_items = player_items

    def add_item_to_inventory(self, new_item: Item):
        self._player_items.append(new_item)

    def drop_item_from_inventory(self, item_to_drop: Item):
        self._player_items.remove(item_to_drop)