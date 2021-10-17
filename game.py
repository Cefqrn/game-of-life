import pygame as pg

from abc import ABC, abstractmethod


class Game(ABC):
    __slots__ = "screen", "sprites", "running"

    def __init__(self, window_width: int, window_height: int, title: str) -> None:
        pg.init()

        self.screen = pg.display.set_mode((window_width, window_height))
        pg.display.set_caption(title)

        self.running = True

    def kill(self) -> None:
        """
        Closes the game
        """
        self.running = False
    
    @abstractmethod
    def on_key_down(self) -> None: pass
    
    @abstractmethod
    def on_mouse_button_down(self) -> None: pass

    @abstractmethod
    def on_loop(self) -> None: pass

    @abstractmethod
    def before_loop(self) -> None: pass

    def on_event(self, event) -> None:
        event_type = event.type
        if event_type == pg.QUIT:
            self.running = False
        elif event_type == pg.MOUSEBUTTONDOWN:
            self.on_mouse_button_down(event.button)
        elif event_type == pg.KEYDOWN:
            self.on_key_down(event.key)

    def main_loop(self) -> None:
        self.before_loop()
        while self.running:
            for event in pg.event.get():
                self.on_event(event)
                
            self.on_loop()
