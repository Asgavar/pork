import pork.aggregates


def test_return_to_start_pos_after_circle():
    world_layout = pork.aggregates.WorldLayout(0, 0)

    world_layout.move_player_north()
    world_layout.move_player_east()
    world_layout.move_player_south()
    world_layout.move_player_west()

    assert world_layout._player_loc == [0, 0]
