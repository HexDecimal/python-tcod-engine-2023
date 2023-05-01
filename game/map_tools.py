import itertools
import random

import attrs
from tcod.ecs import Entity, World

import game.mapgen.caves
from game import map_attrs
from game.components import Context, Graphic, MapDict, Position, Stairway
from game.map import Map, MapKey
from game.tags import ChildOf
from game.tiles import TileDB


@attrs.define(frozen=True)
class TestMap(MapKey):
    level: int = 0

    def generate(self, world: World) -> Entity:
        map = new_map(world, 50, 50)
        free_spaces = list(itertools.product(range(1, 9), range(1, 9)))
        random.shuffle(free_spaces)
        features = [
            world.new_entity(
                [
                    Position(*free_spaces.pop()),
                    Graphic(ord(">")),
                    Stairway(down=game.mapgen.caves.CaveMap(self.level + 1)),
                ]
            ),
        ]

        if self.level > 0:
            features.append(
                world.new_entity(
                    [Position(*free_spaces.pop()), Graphic(ord("<")), Stairway(up=TestMap(self.level - 1))]
                )
            )
        for entity in features:
            entity.relation_tags[ChildOf] = map
        return map


def new_map(world: World, width: int, height: int) -> Entity:
    tile_db = world.global_.components[TileDB]
    map = Map(width, height)
    map[map_attrs.a_tiles][:] = tile_db["wall"]
    map[map_attrs.a_tiles][1:-1, 1:-1] = tile_db["floor"]
    return world.new_entity([map])


def get_map(world: World, key: MapKey) -> Entity:
    map_dict = world.global_.components[MapDict]
    if key not in map_dict:
        map_dict[key] = key.generate(world)
    return map_dict[key]


def activate_map(world: World, key: MapKey) -> Entity:
    new_map = world.global_.components[Context].active_map = get_map(world, key)
    return new_map
