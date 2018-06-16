#!/usr/bin/env python3

import cmd
import sys

import aggregates as a
import content_generation
import messaging
from handlers import command as ch
from handlers import event as evh
from handlers import query as qh
import commands as c
import events as e
import queries as q


class PorkShell(cmd.Cmd):

    prompt = '>>> '

    def __init__(self, world: a.WorldLayout, doors: a.Doors,
                 monsters: a.Monsters, inventory: a.PlayerInventory,
                 command_bus: messaging.CommandBus, event_bus: messaging.EventBus,
                 query_bus: messaging.QueryBus) -> None:
        self.world = world
        self.doors = doors
        self.monsters = monsters
        self.inventory = inventory
        self.command_bus = command_bus
        self.event_bus = event_bus
        self.query_bus = query_bus
        super().__init__()

    def do_ekwipunek(self, arg):
        print(
            f'W plecaku masz {self.inventory.describe_currently_held_items()}'
        )

    def do_idz(self, arg):
        if arg not in ['north', 'east', 'south', 'west']:
            print('to nie jest kierunek!')
            return
        self.command_bus.dispatch(c.MovePlayer(arg))

    def do_popatrz(self, arg):
        print(
            f'Jesteś w {self.world._player_loc} i widzisz '
            f'{self.world.describe_objects_in_the_current_room()}'
        )

    def do_uzyj(self, arg):
        print(f'Używasz {arg}')
        self.command_bus.dispatch(c.UseItem(arg))

    def do_wyjdz(self, arg):
        return True

    def do_zaatakuj(self, arg):
        print(f'Atakujesz {arg}')
        self.command_bus.dispatch(c.AttackMonster(arg))


def run_game(rooms_count: int):
    world = a.WorldLayout()
    doors = a.Doors()
    monsters = a.Monsters()
    inventory = a.PlayerInventory()
    rng = content_generation.PseudoRandomCreationDecider()
    generator = content_generation.WorldGenerator(rng, rooms_count)
    world_map = generator.create_world_map()
    world._world_map = world_map
    generator.process_world_map(world_map, monsters, doors, inventory)

<<<<<<< HEAD
    command_bus = cqrs.CommandBus()
    event_bus = cqrs.EventBus()
    query_bus = cqrs.QueryBus()
    command_router = cqrs.OnlyOneFunctionRouter()
    event_router = cqrs.OnlyOneFunctionRouter()
    query_router = cqrs.OnlyOneFunctionRouter()
=======
    command_bus = messaging.CommandBus()
    event_bus = messaging.EventBus()
    query_bus = messaging.QueryBus()
    command_router = messaging.OnlyOneFunctionRouter()
    event_router = messaging.AllWhichMatchFunctionRouter()
    query_router = messaging.OnlyOneFunctionRouter()
>>>>>>> 7e2d55b... Rename cqrs.py to messaging.py
    command_bus.attach_router(command_router)
    event_bus.attach_router(event_router)
    query_bus.attach_router(query_router)

    use_item_handler = ch.UseItemHandler(event_bus)
    move_player_handler = ch.MovePlayerHandler(world)
    attack_monster_handler = ch.AttackMonsterHandler(monsters, event_bus)
    item_used_handler = evh.ItemUsedHandler(inventory)
    monster_died_handler = evh.MonsterDiedHandler(monsters)
    room_description_handler = qh.DescriptionOfCurrentRoomHandler(world)
    inventory_description_handler = qh.DescriptionOfInventoryHandler(inventory)

    command_router.route_class_to_func(c.UseItem, use_item_handler)
    command_router.route_class_to_func(c.MovePlayer, move_player_handler)
    command_router.route_class_to_func(c.AttackMonster, attack_monster_handler)

    event_router.route_class_to_func(e.ItemUsed, item_used_handler)
    event_router.route_class_to_func(e.MonsterDied, monster_died_handler)

    query_router.route_class_to_func(q.DescriptionOfCurrentRoom,
                                     room_description_handler)
    query_router.route_class_to_func(q.DescriptionOfInventory,
                                     inventory_description_handler)

    shell = PorkShell(world, doors, monsters, inventory,
                      command_bus, event_bus, query_bus)
    shell.cmdloop()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python repl.py <ROOMS_COUNT>')
        sys.exit()
    rooms_count = int(sys.argv[1])
    run_game(rooms_count)
