from typing import Any, TypeVar, overload

from numpy.typing import NDArray

_ScreenArray = TypeVar("_ScreenArray", bound=NDArray[Any])
_WorldArray = TypeVar("_WorldArray", bound=NDArray[Any])


def get_1d_slice(screen_width: int, world_width: int, camera_pos: int) -> tuple[slice, slice]:
    """Return a (screen_slice, world_slice) pair of slices for the given screen/world sizes with the camera position."""
    screen_left = max(0, -camera_pos)
    world_left = max(0, camera_pos)
    screen_width = min(screen_width - screen_left, world_width - world_left)
    return slice(screen_left, screen_left + screen_width), slice(world_left, world_left + screen_width)


@overload
def get_slices(screen: tuple[int], world: tuple[int], camera: tuple[int]) -> tuple[tuple[slice], tuple[slice]]:
    ...


@overload
def get_slices(
    screen: tuple[int, int], world: tuple[int, int], camera: tuple[int, int]
) -> tuple[tuple[slice, slice], tuple[slice, slice]]:
    ...


@overload
def get_slices(
    screen: tuple[int, int, int], world: tuple[int, int, int], camera: tuple[int, int, int]
) -> tuple[tuple[slice, slice, slice], tuple[slice, slice, slice]]:
    ...


@overload
def get_slices(
    screen: tuple[int, ...], world: tuple[int, ...], camera: tuple[int, ...]
) -> tuple[tuple[slice, ...], tuple[slice, ...]]:
    ...


def get_slices(
    screen: tuple[int, ...], world: tuple[int, ...], camera: tuple[int, ...]
) -> tuple[tuple[slice, ...], tuple[slice, ...]]:
    """Return (screen_slice, world_slice) for the given parameters."""
    slices = (get_1d_slice(screen_, world_, camera_) for screen_, world_, camera_ in zip(screen, world, camera))
    screen_slices, world_slices = zip(*slices)
    return tuple(screen_slices), tuple(world_slices)


def get_views(
    screen: _ScreenArray, world: _WorldArray, camera_pos: tuple[int, ...]
) -> tuple[_ScreenArray, _WorldArray]:
    """Return (screen_view, world_view) for the given parameters."""
    screen_slice, world_slice = get_slices(screen.shape, world.shape, camera_pos)
    return screen[screen_slice], world[world_slice]  # type: ignore[return-value]


def clamp_camera_1d(screen_width: int, world_width: int, camera_pos: int, justify: float) -> int:
    right_bound = max(0, world_width - screen_width)
    screen_padding = max(0, screen_width - world_width)
    camera_pos = min(max(0, camera_pos), right_bound)
    camera_pos -= int(screen_padding * justify)
    return camera_pos


def clamp_camera(
    screen: tuple[int, int], world: tuple[int, int], camera: tuple[int, int], justify: tuple[float, float] = (0, 0)
) -> tuple[int, int]:
    return (
        clamp_camera_1d(screen[0], world[0], camera[0], justify[0]),
        clamp_camera_1d(screen[1], world[1], camera[1], justify[1]),
    )
