import tcod
from tcod.camera import clamp_camera, get_views

import g
import game.actions
import game.commands
from game.components import Context, Direction, Graphic, MapFeatures, Position
from game.map import Map
from game.map_attrs import a_tiles
from game.state import State
from game.tiles import tiles_db


class InGame(State):
    def on_event(self, event: tcod.event.Event) -> None:
        match event:
            case tcod.event.KeyDown():
                command = game.commands.keybindings.parse(event=event, enum=game.commands.InGame)
                if command:
                    return self.on_command(command)
            case tcod.event.Quit():
                raise SystemExit()

    def on_command(self, command: game.commands.InGame) -> None:
        match command.value:
            case game.commands.MoveDir(x=dx, y=dy):
                game.actions.Bump([Direction(dx, dy)]).perform(g.world, g.world[Context].player)
            case ">":
                pass

    def on_draw(self, console: tcod.Console) -> None:
        map = g.world[Context].active_map[Map]
        player_pos = g.world[Context].player[Position]
        camera_ij: tuple[int, ...] = (player_pos.y - console.height // 2, player_pos.x - console.width // 2)
        camera_ij = clamp_camera((console.height, console.width), (map.height, map.width), camera_ij)
        screen_view, world_view = get_views(console.tiles_rgb, map[a_tiles], camera_ij)
        screen_view[:] = tiles_db["graphic"][world_view]

        for feature in g.world[Context].active_map[MapFeatures].features:
            pos = feature[Position]
            screen_x = pos.x - camera_ij[1]
            screen_y = pos.y - camera_ij[0]
            if 0 <= screen_x < console.width and 0 <= screen_y < console.height:
                graphic = feature[Graphic]
                console.tiles_rgb[["ch", "fg"]][screen_y, screen_x] = graphic.ch, graphic.fg

        for actor in g.world[Context].actors:
            pos = actor[Position]
            screen_x = pos.x - camera_ij[1]
            screen_y = pos.y - camera_ij[0]
            if 0 <= screen_x < console.width and 0 <= screen_y < console.height:
                graphic = actor[Graphic]
                console.tiles_rgb[["ch", "fg"]][screen_y, screen_x] = graphic.ch, graphic.fg

        console.print(0, 0, f"Turn: {g.world[Context].sched.time}", fg=(255, 255, 255))
