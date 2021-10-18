import pygame as pg


class Game:
    __slots__ = "screen", "sprites", "running", "listeners"

    def __init__(self, window_width: int, window_height: int, title: str) -> None:
        pg.init()

        self.screen = pg.display.set_mode((window_width, window_height))
        pg.display.set_caption(title)

        self.listeners = {
            pg.QUIT: self.kill
        }

        self.running = True

    def kill(self, *_) -> None:
        """
        Closes the game.
        """
        self.running = False
    
    def before_loop(self) -> None: pass
    def on_loop(self) -> None: pass

    def on_event(self, event) -> None:
        """
        Calls the function associated to the type of the event passed in.
        """
        # Listeners must take in the event argument
        self.listeners.get(event.type, lambda _: None)(event)

    def main_loop(self) -> None:
        self.before_loop()
        while self.running:
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
