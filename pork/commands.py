class UseItem:

    def __init__(self, item_name: str) -> None:
        self.item_name = item_name


class MovePlayer:

    def __init__(self, direction: str) -> None:
        self.direction = direction


class AttackMonster:

    def __init__(self, monster_name):
        self.monster_name = monster_name
