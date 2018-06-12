from typing import List
import pytest

from pork.content_generation import (
    PseudoRandomCreationDecider,
    WorldGenerator,
    CreationDecider,
)


def test_is_even():
    rng = PseudoRandomCreationDecider()

    assert rng.is_even(2) is True
    assert rng.is_even(17) is False


def test_mark_rooms_to_be_created(room_count):
    rng = FakeCreationDecider()
    generator = WorldGenerator(rng, room_count)

    list_of_marked_rooms = generator.mark_rooms_to_be_created((0, 0))

    assert len(list_of_marked_rooms) > room_count


@pytest.fixture(params=[1, 5, 15, 50, 200])
def room_count(request):
    return request.param


class FakeCreationDecider(CreationDecider):

    def should_create_one_more_room_north(self) -> bool:
        return True

    def should_create_one_more_room_east(self) -> bool:
        return True

    def should_create_one_more_room_south(self) -> bool:
        return True

    def should_create_one_more_room_west(self) -> bool:
        return True

    def doors_in_which_directions(self) -> List[str]:
        return ['north', 'east', 'south', 'west']

    def how_many_monsters_in_current_room(self) -> int:
        return 10
