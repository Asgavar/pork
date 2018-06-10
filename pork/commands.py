import pork.cqrs


class UseItem(pork.cqrs.Command):

    def __init__(self, item_name: str) -> None:
        self.item_name = item_name


class MovePlayer(pork.cqrs.Command):

    def __init__(self, direction: str) -> None:
        self.direction = direction


class AttackMonster(pork.cqrs.Command):

    def __init__(self, monster_name):
        self.monster_name = monster_name
