import itertools
import random

from tcod.ecs import Entity

import game.mapgen.caves
from game.map import MapKey
from game.map_tools import init_map
from game.travel import force_move, new_stairway


def test_map(map: Entity) -> Entity:
    world = map.world
    map = init_map(map, 50, 50)
    free_spaces = list(itertools.product(range(1, 9), range(1, 9)))
    random.shuffle(free_spaces)
    force_move(new_stairway(world, "down", MapKey(game.mapgen.caves.new_cave, level=1)), free_spaces.pop(), map)

    return map
