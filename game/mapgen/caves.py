"""Cellular automata cave generator."""
from typing import Any

import attrs
import numpy as np
import scipy.ndimage  # type: ignore
import scipy.signal  # type: ignore
from numpy.typing import NDArray
from tcod.ecs import Entity, World

import game.map_tools
import game.mapgen.test
from game import map_attrs
from game.components import Graphic, Position, Stairway
from game.map import Map, MapKey, UniqueMapKey
from game.tags import ChildOf
from game.tiles import TileDB


def get_holes(input: NDArray[Any]) -> NDArray[np.bool_]:
    """Return a boolean map for all sections which are holes."""
    label, num_features = scipy.ndimage.label(input, [[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    max_label = np.argmax([np.sum(label == i) for i in range(1, num_features + 1)]) + 1
    label[label == max_label] = 0
    return label != 0  # type: ignore[no-any-return]


@attrs.define(frozen=True)
class CaveMap(MapKey):
    level: int

    def generate(self, world: World) -> Entity:
        assert self.level > 0
        tiles_db = world.global_.components[TileDB]
        rng = np.random.default_rng()

        map = game.map_tools.new_map(world, 50, 50)
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

        features = [
            world.new_entity([Position(*free_spaces.pop()), Graphic(ord(">")), Stairway(down=CaveMap(self.level + 1))]),
            world.new_entity(
                [
                    Position(*free_spaces.pop()),
                    Graphic(ord("<")),
                    Stairway(
                        up=UniqueMapKey(game.mapgen.test.test_map) if self.level == 1 else CaveMap(self.level - 1)
                    ),
                ]
            ),
        ]
        for entity in features:
            entity.relation_tags[ChildOf] = map

        return map
