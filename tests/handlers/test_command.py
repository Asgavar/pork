import pork.aggregates as a
import pork.commands as c
import pork.entities as e
import pork.messaging
import pork.handlers.command as ch


def test_player_movement():
    command_bus = pork.messaging.CommandBus()
    router = pork.messaging.OnlyOneFunctionRouter()
    command_bus.attach_router(router)
    world_layout = a.WorldLayout()
    handler = ch.MovePlayerHandler(world_layout)
    router.route_class_to_func(c.MovePlayer, handler)

    command_bus.dispatch(c.MovePlayer('north'))
    command_bus.dispatch(c.MovePlayer('north'))
    command_bus.dispatch(c.MovePlayer('east'))
    command_bus.dispatch(c.MovePlayer('north'))

    assert world_layout._player_loc == [1, 3]

    command_bus.dispatch(c.MovePlayer('west'))
    command_bus.dispatch(c.MovePlayer('west'))
    command_bus.dispatch(c.MovePlayer('south'))

    assert world_layout._player_loc == [-1, 2]


class FakeRng:

    def __call__(self):
        return 10


def test_attacking():
    command_bus = pork.messaging.CommandBus()
    router = pork.messaging.OnlyOneFunctionRouter()
    command_bus.attach_router(router)
    monster1_name = 'Przeraźliwy Przedsiębiorca'
    monster1 = e.Monster(monster1_name, 15)
    monster2_name = 'Okropny Oligarcha'
    monster2 = e.Monster(monster2_name, 30)
    monsters = a.Monsters({
        monster1_name: monster1,
        monster2_name: monster2
    })
    rng = FakeRng()
    router.route_class_to_func(
        c.AttackMonster,
        ch.AttackMonsterHandler(monsters, pork.messaging.EventBus(), rng=rng)
    )

    command_bus.dispatch(c.AttackMonster(monster1_name))
    command_bus.dispatch(c.AttackMonster(monster1_name))
    command_bus.dispatch(c.AttackMonster(monster2_name))
    command_bus.dispatch(c.AttackMonster(monster2_name))
    command_bus.dispatch(c.AttackMonster(monster2_name))

    assert monsters.is_monster_dead(monster1_name) is True
    assert monsters.is_monster_dead(monster2_name) is True
    assert monster1.health == -5
    assert monster2.health == 0
