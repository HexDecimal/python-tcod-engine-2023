"""Cellular automata cave generator."""

from typing import Any

import numpy as np
import scipy.ndimage  # type: ignore
import scipy.signal  # type: ignore
from numpy.typing import NDArray
from tcod.ecs import Entity

import game.map_tools
import game.mapgen.test
import game.monsters
from game import map_attrs
from game.action import Action
from game.actions import AttackPlayer
from game.components import Position
from game.map import Map, MapKey
from game.tiles import TileDB
from game.travel import force_move, new_stairway


def get_holes(input: NDArray[Any]) -> NDArray[np.bool_]:
    """Return a boolean map for all sections which are holes."""
    label, num_features = scipy.ndimage.label(input, [[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    max_label = np.argmax([np.sum(label == i) for i in range(1, num_features + 1)]) + 1
    label[label == max_label] = 0
    return label != 0  # type: ignore[no-any-return]


def new_cave(map: Entity, level: int) -> Entity:
    world = map.world
    assert level > 0
    tiles_db = world[None].components[TileDB]
    rng = np.random.default_rng()

    game.map_tools.init_map(map, 50, 50)
    walls = np.zeros((map.components[Map].height - 2, map.components[Map].width - 2), bool)

    walls.ravel()[: walls.size * 45 // 100] = 1
    rng.shuffle(walls.ravel())

    N = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.int8)
    # Rules for neighbor counts.
    OPEN = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1], bool)  # Open space rule.
    CLOSED = np.array([1, 0, 0, 1, 1, 0, 0, 0, 0], bool)  # Closed space rule.
    for _ in range(8):
        # Collect tiles which fit the rules and shuffle the tiles for them.
        neighbors = scipy.signal.convolve(walls, N, "same", "direct")
        unstable = np.where(walls, CLOSED[neighbors], OPEN[neighbors])
        unstable[0, :] |= walls[0, :] == 0
        unstable[-1, :] |= walls[-1, :] == 0
        unstable[:, 0] |= walls[:, 0] == 0
        unstable[:, -1] |= walls[:, -1] == 0
        unstable |= get_holes(walls == 0)
        unstable_where = np.where(unstable)
        unstable_buffer = walls[unstable_where]
        rng.shuffle(unstable_buffer)
        walls[unstable_where] = unstable_buffer

    # Fill holes
    walls[get_holes(walls == 0)] = True

    walls = np.pad(walls, 1, constant_values=True)

    map.components[Map][map_attrs.a_tiles][:] = np.array([tiles_db["floor"], tiles_db["wall"]])[walls.astype(int)]
    free_spaces_ = np.argwhere(walls.T == 0)
    rng.shuffle(free_spaces_)
    free_spaces = free_spaces_.tolist()

    force_move(new_stairway(world, "down", MapKey(new_cave, level + 1)), free_spaces.pop(), map)
    force_move(
        new_stairway(world, "up", MapKey(game.mapgen.test.test_map) if level == 1 else MapKey(new_cave, level - 1)),
        free_spaces.pop(),
        map,
    )

    for _ in range(10):
        ai_actor = game.monsters.spawn("orc", map, Position(*free_spaces.pop()))
        ai_actor.components.update(
            {
                ("ai", Action): AttackPlayer(),
            }
        )
        ai_actor.components[("attack", int)] = 2

    return map
