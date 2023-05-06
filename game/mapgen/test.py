import itertools
import random

import attrs
from tcod.ecs import Entity, World

import game.mapgen.caves
from game.components import Graphic, Position, Stairway
from game.map import MapKey
from game.map_tools import new_map
from game.tags import ChildOf


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
