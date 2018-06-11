import abc
from typing import List


class CreationDecider(abc.ABC):

    @abc.abstractmethod
    def should_create_one_more_room_north() -> bool: pass

    @abc.abstractmethod
    def should_create_one_more_room_east() -> bool: pass

    @abc.abstractmethod
    def should_create_one_more_room_south() -> bool: pass

    @abc.abstractmethod
    def should_create_one_more_room_west() -> bool: pass

    @abc.abstractmethod
    def doors_in_which_directions() -> List[str]: pass

    @abc.abstractmethod
    def how_many_monsters_in_current_room() -> int: pass
