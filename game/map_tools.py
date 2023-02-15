from tcod.ec import ComponentDict

from game import map_attrs
from game.components import Graphic, MapFeatures, Position, Stairway
from game.map import Map


def new_map(width: int, height: int) -> ComponentDict:
    map = Map(width, height)
    map[map_attrs.a_tiles][:] = 1
    map[map_attrs.a_tiles][1:-1, 1:-1] = 0
    map_entity = ComponentDict([map])
    map_entity[MapFeatures] = MapFeatures(
        [
            ComponentDict([Position(3, 3), Graphic(ord(">")), Stairway(("", 1))]),
        ]
    )

    return map_entity
