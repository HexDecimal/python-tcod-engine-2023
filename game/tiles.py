"""Collect and handle tile types."""
from collections.abc import Iterable
from typing import Any

import numpy as np
import tcod
from numpy.typing import NDArray
from tcod.ecs import World

TILE_DTYPE = np.dtype(
    [
        ("graphic", tcod.console.rgb_graphic),
        ("transparent", np.bool_),
        ("walk_cost", np.int8),
    ]
)


class TileDB:
    """Holds a sequence of tiles identified with string names.

    The int ids from this database are stable and will never become invalid.

    The name `""` exists as a null key returning the id of `0`.
    """

    __slots__ = ("data", "_identifiers", "_names", "__weakref__")

    def __init__(self, tiles: Iterable[dict[str, Any]] = ()) -> None:
        self.data: NDArray[Any] = np.zeros((1,), dtype=TILE_DTYPE)
        """The raw data table for this database.

        Access a tiles data with: `tile_db.data[tile_db["name"]]`
        """
        self._names = [""]
        """Tile names in order of definition."""
        self._identifiers: dict[str, int] = {"": 0}
        """Mapping of string keys to tile integer ids."""
        for tile in tiles:
            self.register(**tile)

    def register(
        self,
        name: str,
        *,
        graphic: tuple[int, tuple[int, int, int], tuple[int, int, int]],
        transparent: bool,
        walk_cost: int,
    ) -> None:
        """Add or update a tile name with new data.

        An existing tile is updated with the new parameters without changing its ID.
        """
        tile_id = self._identifiers.get(name)
        if tile_id is None:
            tile_id = len(self._names)
            self._names.append(name)
            self._identifiers[name] = tile_id
            if self.data.size >= tile_id:
                self.data = np.pad(self.data, (0, self.data.size))
        self.data[tile_id] = (graphic, transparent, walk_cost)

    def __getnewargs__(self) -> tuple[list[dict[str, Any]]]:
        """Serialize a database as a list of tiles to be passed to the initializer.

        This helps with tile changes better than if the Numpy array was serialized directly.
        Tile name/id order is preserved so arrays holding an id will not become invalid.
        """
        tiles: list[dict[str, Any]] = []
        for i, name in enumerate(self._names):
            tile = {"name": name}
            assert self.data.dtype.names
            for attr in self.data.dtype.names:
                tile[attr] = self.data[i][attr].tolist()

        return (tiles,)

    def __getitem__(self, key: str) -> int:
        """Return the tile ID for the name `key`."""
        return self._identifiers[key]


def init(world: World) -> None:
    """Initialize or update the TileDB component on a world."""
    if TileDB not in world.global_.components:
        world.global_.components[TileDB] = TileDB()
    tile_db = world.global_.components[TileDB]
    tile_db.register("", graphic=(ord("?"), (0xFF, 0xFF, 0xFF), (0xFF, 0x0, 0xFF)), transparent=True, walk_cost=1)
    tile_db.register("floor", graphic=(ord("."), (0x44, 0x44, 0x44), (0x0, 0x0, 0x0)), transparent=True, walk_cost=1)
    tile_db.register("wall", graphic=(ord(" "), (0xFF, 0xFF, 0xFF), (0x88, 0x88, 0x88)), transparent=False, walk_cost=0)
