import abc
from typing import List


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
