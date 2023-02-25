import tcod

import g
import game.action
import game.actions
import game.actor_tools
import game.commands
import game.rendering
from game.components import Context, Direction
from game.sched import Ticket
from game.state import State


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
        game.rendering.render_map(g.world, console.tiles_rgb)

        console.print(0, 0, f"Turn: {g.world[Context].sched.time}", fg=(255, 255, 255))
