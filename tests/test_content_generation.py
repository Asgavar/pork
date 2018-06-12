import pytest

from pork.content_generation import (
    PseudoRandomCreationDecider,
    WorldGenerator
)


def test_is_even():
    rng = PseudoRandomCreationDecider()

    assert rng.is_even(2) is True
    assert rng.is_even(17) is False


def test_mark_rooms_to_be_created(room_count):
    rng = PseudoRandomCreationDecider()
    generator = WorldGenerator(rng, room_count)

    list_of_marked_rooms = generator.mark_rooms_to_be_created((0, 0))

    assert len(list_of_marked_rooms) >= room_count


@pytest.fixture(params=[5, 15, 50])
def room_count(request):
    return request.param
