from typing import NamedTuple


class UseItem(NamedTuple):

    item_name: str


class MovePlayer(NamedTuple):

    direction: str


class AttackMonster(NamedTuple):

    monster_name: str
