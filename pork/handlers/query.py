import aggregates as a
import queries as q


class DescriptionOfCurrentRoomHandler:

    def __init__(self, world_layout: a.WorldLayout) -> None:
        self.world_layout = world_layout

    def __call__(self, query: q.DescriptionOfCurrentRoom) -> str:
        descriptions = [
            world_item.description()
            for world_item in self.world_layout.objects_in_the_current_room()
        ]
        return f'Rozglądasz się wokół siebie i widzisz: {descriptions}'


class DescriptionOfInventoryHandler:

    def __init__(self, inventory: a.PlayerInventory) -> None:
        self.inventory = inventory

    def __call__(self, query: q.DescriptionOfInventory) -> str:
        descriptions = [
            item.description()
            for item in self.inventory.currently_held_items()
        ]
        return f'W plecaku masz: {descriptions}'
