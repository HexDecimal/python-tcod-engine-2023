from typing import NamedTuple

import numpy as np
import tcod

TILE_DTYPE = np.dtype(
    [
        ("graphic", tcod.console.rgb_graphic),
        ("transparent", np.bool_),
        ("walk_cost", np.int8),
    ]
)


class Tile(NamedTuple):
    graphic: tuple[int, tuple[int, int, int], tuple[int, int, int]]
    transparent: bool
    walk_cost: int


tiles_db = np.array(
    [
        Tile(graphic=(ord(" "), (0xFF, 0xFF, 0xFF), (0x0, 0x0, 0x0)), transparent=True, walk_cost=1),
        Tile(graphic=(ord(" "), (0xFF, 0xFF, 0xFF), (0x88, 0x88, 0x88)), transparent=False, walk_cost=0),
    ],
    dtype=TILE_DTYPE,
)
"Database of tiles."
