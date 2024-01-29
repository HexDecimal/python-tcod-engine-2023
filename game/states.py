"""Specialized state subclasses."""

from collections.abc import Callable, Iterable

import attrs
import tcod.console
import tcod.event

import g
import game.action
import game.actions
import game.actor_tools
import game.commands
import game.rendering
import game.world_logic
from game.components import Context, Direction
from game.state import Reset, State, StateResult


class InGame(State):
    def on_event(self, event: tcod.event.Event) -> StateResult:
        match event:
            case tcod.event.KeyDown():
                command = game.commands.keybindings.parse(event=event, enum=game.commands.InGame)
                if command:
                    return self.on_command(command)
            case tcod.event.Quit():
                raise SystemExit()
        return None

    def on_command(self, command: game.commands.InGame) -> StateResult:
        match command.value:
            case game.commands.MoveDir(x=dx, y=dy):
                self.do_action(game.actions.Bump([Direction(dx, dy)]))
            case ">":
                self.do_action(game.actions.UseStairs(["down"]))
            case "<":
                self.do_action(game.actions.UseStairs(["up"]))
        return None

    def do_action(self, action: game.action.Action) -> StateResult:
        game.world_logic.do_action(g.world[None].components[Context].player, action)
        return None

    def on_draw(self, console: tcod.console.Console) -> None:
        game.rendering.render_all(g.world, console)


@attrs.define
class MenuItem:
    label: str
    callback: Callable[[], StateResult]


class Menu(State):
    def __init__(
        self,
        items: Iterable[MenuItem],
        *,
        selected: int = 0,
        x: int = 5,
        y: int = 5,
    ) -> None:
        self.items = list(items)
        self.selected: int | None = selected
        """Index of the focused menu item or None if no item is focused."""
        self.x = x
        self.y = y

    def get_position(self, event: tcod.event.MouseButtonEvent | tcod.event.MouseMotion) -> int | None:
        """Return the menu position of a mouse event."""
        cursor_y = event.position.y - self.y
        if 0 <= cursor_y < len(self.items):
            return cursor_y
        return None

    def on_event(self, event: tcod.event.Event) -> StateResult:
        match event:
            case tcod.event.KeyDown():
                command = game.commands.keybindings.parse(
                    event=event, enum=game.commands.System
                ) or game.commands.keybindings.parse(event=event, enum=game.commands.InGame)
                if command:
                    return self.on_command(command)
            case tcod.event.MouseMotion(motion=motion):
                if motion.x == 0 and motion.y == 0:
                    return None
                self.selected = self.get_position(event)
            case tcod.event.MouseButtonUp(button=tcod.event.BUTTON_LEFT):
                self.selected = self.get_position(event)
                if self.selected is not None:
                    return self.items[self.selected].callback()
                return self.on_cancel()
            case tcod.event.MouseButtonUp(button=tcod.event.BUTTON_RIGHT):
                return self.on_cancel()
            case tcod.event.WindowEvent(type="WindowLeave"):
                self.selected = None
            case tcod.event.Quit():
                raise SystemExit()
        return None

    def on_command(self, command: game.commands.System | game.commands.InGame) -> StateResult:
        match command.value:
            case game.commands.MoveDir(y=dy):
                if self.selected is None:
                    self.selected = 0 if dy > 0 else -1
                else:
                    self.selected += dy
                self.selected %= len(self.items)
            case "CONFIRM":
                if self.selected is not None:
                    return self.items[self.selected].callback()
            case "ESCAPE":
                return self.on_cancel()
        return None

    def on_draw(self, console: tcod.console.Console) -> None:
        this_index = g.state.index(self)
        if this_index > 0:
            g.state[this_index - 1].on_draw(console)
        for i, item in enumerate(self.items):
            bg = (0x40, 0x40, 0x40) if i == self.selected else (0, 0, 0)
            console.print_box(self.x, self.y + i, 0, 0, item.label, fg=(255, 255, 255), bg=bg)

    def on_cancel(self) -> StateResult:
        return None


class MainMenu(Menu):
    def __init__(self) -> None:
        super().__init__(
            [
                MenuItem("New game", self.new_game),
                MenuItem("Quit", self.quit),
            ]
        )

    def new_game(self) -> StateResult:
        return Reset(InGame())

    def quit(self) -> StateResult:
        raise SystemExit()
