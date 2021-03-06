import pork.aggregates as a
import pork.actions as act
import pork.commands as c
import pork.messaging
import pork.entities as e
import pork.events as ev
import pork.handlers.command as ch
import pork.handlers.event as evh


def test_door_opening_after_item_usage():
    event_bus = pork.messaging.EventBus()
    router = pork.messaging.AllWhichMatchFunctionRouter()
    event_bus.attach_router(router)
    door_0_0_north = e.Door('door_0_0_north', 'north')
    doors_aggregate = a.Doors({
        door_0_0_north._door_name: door_0_0_north,
    })
    item_used_mapping = {
        'przedmiocik': act.OpenDoorAction('door_0_0_north', doors_aggregate),
    }
    inventory = a.PlayerInventory(item_action_mapping=item_used_mapping)
    handler = evh.ItemUsedHandler(inventory)
    router.route_class_to_func(ev.ItemUsed, handler)

    assert door_0_0_north.is_open is False
    event_bus.dispatch(ev.ItemUsed('przedmiocik'))
    assert door_0_0_north.is_open is True


def test_item_spawning_after_killing_monster():
    event_bus = pork.messaging.EventBus()
    event_router = pork.messaging.AllWhichMatchFunctionRouter()
    event_bus.attach_router(event_router)
    command_bus = pork.messaging.CommandBus()
    command_router = pork.messaging.OnlyOneFunctionRouter()
    command_bus.attach_router(command_router)
    monster_name = 'groźny potwór boję się go'
    monster = e.Monster(monster_name, 0)
    item = e.Item('pewne coś')
    inventory = a.PlayerInventory()
    monsters_aggregate = a.Monsters({
        monster_name: monster
    }, {
        monster_name: act.SpawnItemInInventoryAction(item, inventory)
    })
    handler = evh.MonsterDiedHandler(monsters_aggregate)
    attack_handler = ch.AttackMonsterHandler(monsters_aggregate, event_bus)
    event_router.route_class_to_func(ev.MonsterDied, handler)
    command_router.route_class_to_func(c.AttackMonster, attack_handler)

    assert item not in inventory.currently_held_items()
    command_bus.dispatch(c.AttackMonster(monster_name))
    assert item in inventory.currently_held_items()
