"""Tools for working with maps."""

from tcod.ecs import Entity, World

from game import map_attrs
from game.components import Context
from game.map import Map, MapKey
from game.tiles import TileDB


def init_map(entity: Entity, width: int, height: int) -> Entity:
    """Return a new map with a simple blank default."""
    tile_db = entity.world[None].components[TileDB]
    map = entity.components[Map] = Map(width, height)
    map[map_attrs.a_tiles][:] = tile_db["wall"]
    map[map_attrs.a_tiles][1:-1, 1:-1] = tile_db["floor"]
    return entity


def get_map(world: World, key: MapKey) -> Entity:
    """Return a map from a MapKey, generating it if required."""
    map = world[key]
    if "IsGenerated" not in map.tags:
        key.generator(map, **dict(key.kwargs))
        map.tags.add("IsGenerated")
    return map


def activate_map(world: World, key: MapKey) -> Entity:
    """Set a map as active and return it."""
    world[None].components[Context].active_map = new_map = get_map(world, key)
    return new_map
