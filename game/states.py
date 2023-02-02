import tcod
from tcod.camera import clamp_camera, get_views

import g
from game.components import Context, Graphic, Position
from game.map import Map
from game.map_attrs import a_tiles
from game.sched import Ticket
from game.state import State
from game.tiles import tiles_db

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}


WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}


class InGame(State):
    def on_event(self, event: tcod.event.Event) -> None:
        match event:
            case tcod.event.KeyDown(sym=sym):
                if sym in MOVE_KEYS:
                    player_pos = g.world[Context].player[Position]
                    dx, dy = MOVE_KEYS[sym]
                    new_x, new_y = player_pos.x + dx, player_pos.y + dy
                    if tiles_db["walk_cost"][g.world[Context].active_map[Map][a_tiles][new_y, new_x]] > 0:
                        player_pos.x += dx
                        player_pos.y += dy
                        g.world[Context].player[Ticket] = g.world[Context].sched.schedule(100, g.world[Context].player)

            case tcod.event.Quit():
                raise SystemExit()

    def on_draw(self, console: tcod.Console) -> None:
        map = g.world[Context].active_map[Map]
        player_pos = g.world[Context].player[Position]
        camera_ij: tuple[int, ...] = (player_pos.y - console.height // 2, player_pos.x - console.width // 2)
        camera_ij = clamp_camera((console.height, console.width), (map.height, map.width), camera_ij)
        screen_view, world_view = get_views(console.tiles_rgb, map[a_tiles], camera_ij)
        screen_view[:] = tiles_db["graphic"][world_view]

        for actor in g.world[Context].actors:
            pos = actor[Position]
            screen_x = pos.x - camera_ij[1]
            screen_y = pos.y - camera_ij[0]
            if 0 <= screen_x < console.width and 0 <= screen_y < console.height:
                graphic = actor[Graphic]
                console.tiles_rgb[["ch", "fg"]][screen_y, screen_x] = graphic.ch, graphic.fg
