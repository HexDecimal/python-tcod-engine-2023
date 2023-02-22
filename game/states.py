import itertools

import tcod
from tcod.camera import clamp_camera, get_views

import g
import game.action
import game.actions
import game.commands
import game.world_logic
from game.components import Context, Direction, Graphic, MapFeatures, Position
from game.map import Map
from game.map_attrs import a_tiles
from game.sched import Ticket
from game.state import State
from game.tiles import TileDB


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
                self.do_action(game.actions.Bump([Direction(dx, dy)]))
            case ">":
                self.do_action(game.actions.UseStairs(["down"]))
            case "<":
                self.do_action(game.actions.UseStairs(["up"]))

    def do_action(self, action: game.action.Action) -> None:
        world = g.world
        player = world[Context].player
        match action.perform(world, player):
            case game.action.Success(time_passed=time_passed):
                assert world[Context].sched.peek() is player[Ticket]
                world[Context].sched.pop()
                player[Ticket] = world[Context].sched.schedule(time_passed, player)
            case game.action.Impossible(reason=reason):
                print(reason)
            case _:
                raise NotImplementedError()

    def on_draw(self, console: tcod.Console) -> None:
        map = g.world[Context].active_map[Map]
        tiles_db = g.world[TileDB]
        player_pos = g.world[Context].player[Position]
        camera_ij: tuple[int, ...] = (player_pos.y - console.height // 2, player_pos.x - console.width // 2)
        camera_ij = clamp_camera((console.height, console.width), (map.height, map.width), camera_ij)
        screen_view, world_view = get_views(console.tiles_rgb, map[a_tiles], camera_ij)
        screen_view[:] = tiles_db.data["graphic"][world_view]

        for obj in itertools.chain(
            g.world[Context].active_map[MapFeatures].features,
            g.world[Context].actors,
        ):
            pos = obj[Position]
            screen_x = pos.x - camera_ij[1]
            screen_y = pos.y - camera_ij[0]
            if 0 <= screen_x < console.width and 0 <= screen_y < console.height:
                graphic = obj[Graphic]
                console.tiles_rgb[["ch", "fg"]][screen_y, screen_x] = graphic.ch, graphic.fg

        console.print(0, 0, f"Turn: {g.world[Context].sched.time}", fg=(255, 255, 255))
