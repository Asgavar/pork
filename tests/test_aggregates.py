import pork.aggregates
import pork.entities


def test_return_to_start_pos_after_circle():
    world_layout = pork.aggregates.WorldLayout(0, 0)

    world_layout.move_player_north()
    world_layout.move_player_east()
    world_layout.move_player_south()
    world_layout.move_player_west()

    assert world_layout._player_loc == [0, 0]


def test_door_path_blocking():
    north_door = pork.entities.Door('door1', 'north')
    east_door = pork.entities.Door('door2', 'east')
    south_door = pork.entities.Door('door3', 'south')
    west_door = pork.entities.Door('door4', 'west')
    world_map = {
        (0, 0): [
            north_door, east_door, south_door, west_door
        ]
    }
    world_layout = pork.aggregates.WorldLayout(0, 0, world_map=world_map)

    world_layout.move_player_north()
    assert world_layout._player_loc == [0, 0]
    world_layout.move_player_east()
    assert world_layout._player_loc == [0, 0]
    world_layout.move_player_south()
    assert world_layout._player_loc == [0, 0]
    world_layout.move_player_west()
    assert world_layout._player_loc == [0, 0]
