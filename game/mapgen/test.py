import itertools
import random

from tcod.ecs import Entity, World

import game.mapgen.caves
from game.components import Graphic, Position, Stairway
from game.map import MapKey
from game.map_tools import new_map
from game.tags import ChildOf


def test_map(world: World) -> Entity:
    map = new_map(world, 50, 50)
    free_spaces = list(itertools.product(range(1, 9), range(1, 9)))
    random.shuffle(free_spaces)
    features = [
        world.new_entity(
            [
                Position(*free_spaces.pop()),
                Graphic(ord(">")),
                Stairway(down=MapKey(game.mapgen.caves.new_cave, level=1)),
            ]
        ),
    ]

    for entity in features:
        entity.relation_tags[ChildOf] = map
    return map
