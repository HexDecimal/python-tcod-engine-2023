from snecs import Component, register_component
from snecs.typedefs import EntityID


@register_component
class Globals(Component):
    active_map: EntityID = EntityID(0)
    player: EntityID = EntityID(0)


@register_component
class Position(Component):
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
