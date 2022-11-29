from typing import Optional, Type, TypeVar

import snecs
from snecs import World
from snecs.bound_world import BoundWorld
from snecs.typedefs import EntityID

__all__ = (
    "WorldWithContext",
    "BoundEntity",
)

T = TypeVar("T")


class WorldWithContext(BoundWorld):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.context = self.new_entity()
        "A global entity used for important components."


class BoundEntity(EntityID):
    def __new__(cls, entity: EntityID, world: World):
        self = cls(entity)
        self.world = world

    def __getitem__(self, key: Type[T]) -> T:
        return snecs.entity_component(self, key, self.world)
