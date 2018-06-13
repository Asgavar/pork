import pork.aggregates as a
import pork.cqrs
import pork.entities as e
import pork.handlers.query as qh
import pork.queries as q


def test_description_of_current_room():
    querybus = pork.cqrs.QueryBus()
    router = pork.cqrs.OnlyOneFunctionRouter()
    querybus.attach_router(router)
    some_door = e.Door('north_doors_0_0', 'north')
    some_monster = e.Monster('Wielki Groźny Szczur', 100)
    some_item = e.Item('Magiczny Miecz')
    world_map = {
        (0, 0): [
            some_door, some_monster, some_item
        ]
    }
    world_layout = a.WorldLayout(world_map=world_map)
    handler = qh.DescriptionOfCurrentRoomHandler(world_layout)
    router.route_class_to_func(q.DescriptionOfCurrentRoom, handler)

    returned_description = querybus.dispatch(q.DescriptionOfCurrentRoom())

    assert 'Drzwi' in returned_description
    assert 'north' in returned_description
    assert 'Potwór' in returned_description
    assert 'Szczur' in returned_description
    assert 'Przedmiot' in returned_description
    assert 'Miecz' in returned_description


def test_description_of_inventory():
    querybus = pork.cqrs.QueryBus()
    router = pork.cqrs.OnlyOneFunctionRouter()
    querybus.attach_router(router)
    item1 = e.Item('Kijek Prawdy')
    item2 = e.Item('Patyk Kłamstwa')
    inventory = a.PlayerInventory()
    router.route_class_to_func(
        q.DescriptionOfInventory,
        qh.DescriptionOfInventoryHandler(inventory)
    )

    inventory.add_item_to_inventory(item1)
    inventory.add_item_to_inventory(item2)
    returned_description = querybus.dispatch(q.DescriptionOfInventory())

    assert 'Kijek Prawdy' in returned_description
    assert 'Patyk Kłamstwa' in returned_description
