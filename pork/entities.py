import abc


class WorldObject(abc.ABC):

    @abc.abstractmethod
    def description(self) -> str:
        pass


class Door(WorldObject):

    def __init__(self, door_name: str, door_direction: str,
                 is_open: bool = False) -> None:
        self._door_name = door_name
        self.door_direction = door_direction
        self.is_open = is_open

    def description(self) -> str:
        proper_word = 'otwierają' if self.is_open else 'blokują'
        return f'Drzwi, które {proper_word} przejście do {self.door_direction}'


class Item(WorldObject):

    def __init__(self, item_name: str) -> None:
        self._item_name = item_name

    def description(self) -> str:
        return f'Przedmiot o nazwie {self._item_name}'


class Monster(WorldObject):

    def __init__(self, monster_name: str, health: int) -> None:
        self.monster_name = monster_name
        self.health = health

    def description(self) -> str:
        return f'Potwór o nazwie {self.monster_name} i HP = {self.health}'
