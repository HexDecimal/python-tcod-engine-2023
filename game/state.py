import tcod


class State:
    def on_event(self, event: tcod.event.Event) -> None:
        pass

    def on_draw(self, console: tcod.Console) -> None:
        pass
