import abc


class WorldObject(abc.ABC):

    @abc.abstractmethod
    def description(self) -> str:
        pass


class Door(WorldObject):

    def __init__(self, door_name: str) -> None:
        self._door_name = door_name

    def description(self) -> str:
        return f'Drzwi o nazwie {self._door_name}'


class Item(WorldObject):

    def __init__(self, item_name: str, action_triggered) -> None:
        self._item_name = item_name

    def description(self) -> str:
        return f'Przedmiot o nazwie {self._item_name}'
