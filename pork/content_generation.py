import abc
import random
from typing import Dict, List, Tuple

from pork.aggregates import Doors, Monsters, WorldLayout
from pork.entities import Item, WorldObject


class CreationDecider(abc.ABC):

    @abc.abstractmethod
    def should_create_one_more_room_north(self) -> bool: pass

    @abc.abstractmethod
    def should_create_one_more_room_east(self) -> bool: pass

    @abc.abstractmethod
    def should_create_one_more_room_south(self) -> bool: pass

    @abc.abstractmethod
    def should_create_one_more_room_west(self) -> bool: pass

    @abc.abstractmethod
    def doors_in_which_directions(self) -> List[str]: pass

    @abc.abstractmethod
    def how_many_monsters_in_current_room(self) -> int: pass


class PseudoRandomCreationDecider(CreationDecider):

    def should_create_one_more_room_north(self) -> bool:
        return self.is_even(self.roll()[0])

    def should_create_one_more_room_east(self) -> bool:
        return self.is_even(self.roll()[1])

    def should_create_one_more_room_south(self) -> bool:
        return self.is_even(self.roll()[2])

    def should_create_one_more_room_west(self) -> bool:
        return self.is_even(self.roll()[3])

    def doors_in_which_directions(self) -> List[str]:
        directions = ['north', 'east', 'south', 'west']
        roll_result = self.roll()
        return [
            directions[_] for _ in range(4) if self.is_even(roll_result[_])
        ]

    def how_many_monsters_in_current_room(self) -> int:
        return int(self.roll()) % 10

    @staticmethod
    def roll() -> str:
        return str(random.randint(1000, 9999))

    @staticmethod
    def is_even(n_str: str) -> bool:
        return '{:b}'.format(int(n_str))[-1] == '0'


XYTuple = Tuple[int, int]


class WorldGenerator:

    def __init__(self, decider: CreationDecider, how_many_rooms: int) -> None:
        self.decider = decider
        self.how_many_rooms = how_many_rooms
        self.marked_so_far = 0

    def create_world_map(self) -> Dict[Tuple, List[WorldObject]]:
        pass

    def create_room(self) -> List[WorldObject]:
        pass

    def create_door(self, direction: str):
        pass

    def create_monster(self, monsters: Monsters, item_dropped: Item):
        # TODO: monster died mapping
        pass

    def mark_rooms_to_be_created(self, current_pos: XYTuple) -> List[XYTuple]:
        branches_from_here = []
        self.marked_so_far += 1

        if self.decider.should_create_one_more_room_north():
            branches_from_here.append((current_pos[0], current_pos[1] + 1))
        if self.decider.should_create_one_more_room_east():
            branches_from_here.append((current_pos[0] + 1, current_pos[1]))
        if self.decider.should_create_one_more_room_south():
            branches_from_here.append((current_pos[0], current_pos[1] - 1))
        if self.decider.should_create_one_more_room_west():
            branches_from_here.append((current_pos[0] - 1, current_pos[1]))

        if self.marked_so_far >= self.how_many_rooms:
            return branches_from_here

        branches_from_branches = []
        random.shuffle(branches_from_here)
        for branch in branches_from_here:
            branches_from_branches.extend(
                self.mark_rooms_to_be_created(branch)
            )

        return branches_from_here + branches_from_branches

    def process_world_map(self, world_layout: WorldLayout,
                          monsters: Monsters, doors: Doors):
        pass
