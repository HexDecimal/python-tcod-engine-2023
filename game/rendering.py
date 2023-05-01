import itertools
from typing import Any

import numpy as np
import tcod.camera
import tcod.console
from numpy.typing import NDArray
from tcod.ecs import World

import game.actor_tools
from game.components import Context, Graphic, Position
from game.map import Map
from game.map_attrs import a_tiles
from game.messages import MessageLog
from game.tags import IsActor
from game.tiles import TileDB

SHROUD = np.array([(0x20, (0, 0, 0), (0, 0, 0))], dtype=tcod.console.rgb_graphic)


def render_all(world: World, console: tcod.console.Console) -> None:
    LOG_HEIGHT = 5
    SIDEBAR_WIDTH = 20
    console.clear()
    # if __debug__:
    #    console.rgb[:] = 0x20, (0, 127, 0), (255, 0, 255)
    render_map(world, console.rgb[:-LOG_HEIGHT, :-SIDEBAR_WIDTH])
    log_console = tcod.console.Console(console.width - SIDEBAR_WIDTH, LOG_HEIGHT)
    side_console = tcod.console.Console(SIDEBAR_WIDTH, console.height)

    y = log_console.height
    for message in reversed(world.global_.components[MessageLog].log):
        text = str(message)
        y -= tcod.console.get_height_rect(log_console.width, text)
        log_console.print_box(0, y, log_console.width, 0, text, (255, 255, 255))
        if y <= 0:
            break
    log_console.blit(console, dest_x=0, dest_y=console.height - log_console.height)

    side_console.print(0, 0, f"Turn: {world.global_.components[Context].sched.time}", fg=(255, 255, 255))
    side_console.blit(console, dest_x=console.width - side_console.width, dest_y=0)


def render_map(world: World, out: NDArray[Any]) -> None:
    """Render the active world map, showing visible and remembered tiles/objects."""
    map = world.global_.components[Context].active_map
    map_data = map.components[Map]
    player = world.global_.components[Context].player
    tiles_db = world.global_.components[TileDB]
    player_pos = player.components[Position]
    player_memory = game.actor_tools.get_memory(world, player)
    player_fov = game.actor_tools.compute_fov(world, player)
    camera_ij = tcod.camera.get_camera(out.shape, player_pos.yx, ((map_data.height, map_data.width), 0.5))

    screen_slice, world_slice = tcod.camera.get_slices(out.shape, (map_data.height, map_data.width), camera_ij)
    world_view = map_data[a_tiles][world_slice]

    visible_graphics = tiles_db.data["graphic"][world_view]

    for obj in itertools.chain(
        world.Q.all_of([Position, Graphic], relations=[("ChildOf", map)]).none_of(tags=[IsActor]),
        world.Q.all_of([Position, Graphic], tags=[IsActor], relations=[("ChildOf", map)]),
    ):
        pos = obj.components[Position]
        screen_x = pos.x - camera_ij[1] - screen_slice[1].start
        screen_y = pos.y - camera_ij[0] - screen_slice[0].start
        if 0 <= screen_x < visible_graphics.shape[1] and 0 <= screen_y < visible_graphics.shape[0]:
            graphic = obj.components[Graphic]
            visible_graphics[["ch", "fg"]][screen_y, screen_x] = graphic.ch, graphic.fg

    memory_graphics = tiles_db.data["graphic"][player_memory.tiles[world_slice]]

    for pos, obj in player_memory.objs.items():
        screen_x = pos.x - camera_ij[1] - screen_slice[1].start
        screen_y = pos.y - camera_ij[0] - screen_slice[0].start
        if 0 <= screen_x < visible_graphics.shape[1] and 0 <= screen_y < visible_graphics.shape[0]:
            graphic = obj.components[Graphic]
            memory_graphics[["ch", "fg"]][screen_y, screen_x] = graphic.ch, graphic.fg

    memory_graphics["fg"] //= 2
    memory_graphics["bg"] //= 2

    out[screen_slice] = np.select(
        [player_fov.visible[world_slice], player_memory.tiles[world_slice] != 0],
        [visible_graphics, memory_graphics],
        SHROUD,
    )
