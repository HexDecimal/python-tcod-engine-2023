import tcod

from game.state import State


class HelloWorld(State):
    def on_event(self, event: tcod.event.Event) -> None:
        match event:
            case tcod.event.Quit():
                raise SystemExit()

    def on_draw(self, console: tcod.Console) -> None:
        console.print(0, 0, "Hello world.")
