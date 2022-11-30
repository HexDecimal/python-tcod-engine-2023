from game import map_attrs
from game.entity import Entity
from game.map import Map


def new_map(width: int, height: int) -> Entity:
    map = Map(width, height)
    map[map_attrs.a_tiles][:] = 1
    map[map_attrs.a_tiles][1:-1, 1:-1] = 0
    return Entity(map)
