import abc
import random
from typing import Dict, List, Tuple
import uuid

from actions import OpenDoorAction, SpawnItemInInventoryAction
from aggregates import Doors, Monsters, PlayerInventory
from entities import Door, Item, Monster, WorldObject


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
        return int(self.roll()) % 10 + 1

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

    def create_world_map(self) -> Dict[Tuple[int, int], List[WorldObject]]:
        STARTING_POSITION = (0, 0)
        world_map = {
            coords: self.create_room(coords)
            for coords in self.mark_rooms_to_be_created(STARTING_POSITION)
        }

        return world_map

    def create_room(self, coords: XYTuple) -> List[WorldObject]:
        room_as_list = [
            self.create_monster()
            for _ in range(self.decider.how_many_monsters_in_current_room())
        ]
        door_directions = self.decider.doors_in_which_directions()
        possible_directions = ['north', 'east', 'south', 'west']
        doors_in_room = [
            self.create_door(coords, direction)
            for direction in possible_directions
            if direction in door_directions
        ]
        room_as_list.extend(doors_in_room)

        return room_as_list

    def create_door(self, coords: XYTuple, direction: str) -> Door:
        door_name = 'door_'+str(coords[0])+'_'+str(coords[1])+'_'+direction
        return Door(door_name, direction)

    def create_monster(self):
        MONSTER_MAX_HEALTH = 100
        monster_name = 'potwór_'+str(uuid.uuid4())[0:8]
        return Monster(monster_name, MONSTER_MAX_HEALTH)

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

    def process_world_map(self, world_map: Dict[Tuple, List[WorldObject]],
                          monsters: Monsters, doors: Doors,
                          inventory: PlayerInventory) -> None:
        for coord, room in world_map.items():
            room_doors = list(
                filter(lambda elem: isinstance(elem, Door), room)
            )
            room_monsters = list(
                filter(lambda elem: isinstance(elem, Monster), room)
            )
            for door in room_doors:
                item_to_open = Item(door._door_name+'_opener')
                monster_w_item: Monster = random.choice(room_monsters)
                while monster_w_item in monsters.monster_action_mapping.keys():
                    monster_w_item = random.choice(room_monsters)
                open_door_action = OpenDoorAction(door._door_name, doors)
                spawn_item_action = SpawnItemInInventoryAction(
                    item_to_open, inventory
                )
                doors._doors_lookup[door._door_name] = door
                inventory.item_action_mapping[item_to_open._item_name] =\
                    open_door_action
                monsters.monster_action_mapping[monster_w_item.monster_name] =\
                    spawn_item_action
