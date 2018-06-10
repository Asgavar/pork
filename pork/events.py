import pork.cqrs


class ItemUsed(pork.cqrs.Event):

    def __init__(self, item_name):
        self.item_name = item_name


class MonsterDied(pork.cqrs.Event):

    def __init__(self, monster_name):
        self.monster_name = monster_name
