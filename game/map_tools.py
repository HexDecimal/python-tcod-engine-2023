"""Tools for working with maps."""

from tcod.ecs import Entity, World

from game import map_attrs
from game.components import Context, MapDict
from game.map import Map, MapKey
from game.tiles import TileDB


def new_map(world: World, width: int, height: int) -> Entity:
    """Return a new map with a simple blank default."""
    tile_db = world.global_.components[TileDB]
    map = Map(width, height)
    map[map_attrs.a_tiles][:] = tile_db["wall"]
    map[map_attrs.a_tiles][1:-1, 1:-1] = tile_db["floor"]
    return world.new_entity([map])


def get_map(world: World, key: MapKey) -> Entity:
    """Return a map from a MapKey, generating it if required."""
    map_dict = world.global_.components[MapDict]
    if key not in map_dict:
        map_dict[key] = key.generate(world)
    return map_dict[key]


def activate_map(world: World, key: MapKey) -> Entity:
    """Set a map as active and return it."""
    world.global_.components[Context].active_map = new_map = get_map(world, key)
    return new_map
