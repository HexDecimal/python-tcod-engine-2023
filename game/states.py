import tcod

import g
from game.camera import get_views
from game.components import Context, Position
from game.map import Map
from game.map_attrs import a_tiles
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


class HelloWorld(State):
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
            case tcod.event.Quit():
                raise SystemExit()

    def on_draw(self, console: tcod.Console) -> None:
        map = g.world[Context].active_map[Map]
        pos = g.world[Context].player[Position]
        camera_ij = (pos.y - console.height // 2, pos.x - console.width // 2)
        screen_view, world_view = get_views(console.tiles_rgb, map[a_tiles], camera_ij)
        screen_view[:] = tiles_db["graphic"][world_view]

        console.print(pos.x - camera_ij[1], pos.y - camera_ij[0], "@")
