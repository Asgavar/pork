import random

import aggregates as a
import commands as c
import messaging
import events as ev


class UseItemHandler:

    def __init__(self, event_bus: messaging.EventBus) -> None:
        self.event_bus = event_bus

    def __call__(self, command: c.UseItem):
        self.event_bus.dispatch(ev.ItemUsed(command.item_name))


class MovePlayerHandler:

    def __init__(self, world_layout: a.WorldLayout) -> None:
        self.world_layout = world_layout

    def __call__(self, command: c.MovePlayer):
        direction_mapping = {
            'north': self.world_layout.move_player_north,
            'east': self.world_layout.move_player_east,
            'south': self.world_layout.move_player_south,
            'west': self.world_layout.move_player_west,
        }
        direction_mapping[command.direction]()


class RandomRandintTo100:

    def __call__(self):
        return random.randint(0, 100)


class AttackMonsterHandler:

    def __init__(self, monsters: a.Monsters, event_bus: messaging.EventBus,
                 rng=RandomRandintTo100()) -> None:
        self.rng = rng
        self.monsters = monsters
        self.event_bus = event_bus

    def __call__(self, command: c.AttackMonster):
        attack_power = self.rng()
        self.monsters.attack(command.monster_name, attack_power)
        if self.monsters.is_monster_dead(command.monster_name):
            self.event_bus.dispatch(ev.MonsterDied(command.monster_name))
