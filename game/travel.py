"""Module for handling movement and position."""
from typing import Literal

from tcod.ecs import Entity, World

from game.components import Graphic, Position
from game.map import MapKey
from game.tags import ChildOf

STAIRS_GRAPHICS = {
    "up": Graphic(ord("<")),
    "down": Graphic(ord(">")),
}


def new_stairway(world: World, direction: Literal["up", "down"], dest: MapKey) -> Entity:
    """Return a new stairway entity, not assigned to a location."""
    entity = world.new_entity()
    entity.components[Graphic] = STAIRS_GRAPHICS[direction]
    entity.tags.add("IsStairway")
    entity.relation_tag[direction] = world[dest]
    return entity


def force_move(entity: Entity, xy: Position | tuple[int, int], map: Entity | None) -> Entity:
    """Force move an entity to the given position."""
    entity.components[Position] = xy if isinstance(xy, Position) else Position(*xy)
    if map is not None:
        entity.relation_tag[ChildOf] = map
    assert ChildOf in entity.relation_tag
    return entity
