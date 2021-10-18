from cell_grid import CellGrid
from game import Game

import pygame as pg
import numpy as np

from math import floor

LIVING_CELL_COLOR = pg.Color(0, 255, 0)
DEAD_CELL_COLOR = pg.Color(15, 15, 15)


class GameOfLife(Game):
    __slots__ = "screen", "running", "updating", "cell_grid", "cell_width", "cell_height", "keybinds", "listeners"

    def __init__(self, window_width: int, window_height: int, grid_width: int, grid_height: int, randomize: bool=False) -> None:
        super().__init__(window_width, window_height, "Game of Life")
        pg.event.set_blocked(None)
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN])

        self.cell_grid = CellGrid(grid_width, grid_height)
        self.cell_width = round(window_width/grid_width)
        self.cell_height = round(window_height/grid_height)

        self.updating = False

        self.keybinds = {
            pg.K_SPACE: self.toggle_updating,
            pg.K_RIGHT: self.update_cells,
            pg.K_r: self.randomize,
            pg.K_c: self.cell_grid.clear,
            pg.K_ESCAPE: self.kill
        }

        self.listeners = {
            **self.listeners,
            pg.MOUSEBUTTONDOWN: self.on_mouse_button_down,
            pg.KEYDOWN: self.on_key_down
        }

        if randomize:
            self.randomize()

    def randomize(self, odds: int=8) -> None:
        """
        Sets the grid to a random configuration.
        The odds of a cell being alive are 1/`odds`.
        """
        self.cell_grid.randomize(odds)
    
    def clear(self):
        """
        Kills all the cells in the grid.
        """
        self.cell_grid.clear()
    
    def toggle_updating(self) -> None:
        """
        Toggles the cell grid updating every frame.
        """
        self.updating = not self.updating

    def update_cells(self) -> None:
        """
        Updates the cells following modified rules of Conway's Game of Life,
        modified because a cell's neighbours include the cell itself.
        """
        # Can't seem to reshape the neighbors outside of here
        updated_cells = self.cell_grid.cell_neighbors.reshape(self.cell_grid.width, self.cell_grid.height, -1).sum(2)
        
        # Cell stays the same if the cell has 4 neighbors
        self.cell_grid.cells &= updated_cells == 4
        # Revives the cell if it has 3 neighbors
        self.cell_grid.cells |= updated_cells == 3

    def draw_cell_rect(self, cell_x: float, cell_y: float) -> None:
        """
        Draws a rectangle representing a cell.
        """
        x_pos = cell_x*self.cell_width
        y_pos = cell_y*self.cell_height
        rect = pg.Rect(x_pos, y_pos, self.cell_width, self.cell_height)
        pg.draw.rect(self.screen, LIVING_CELL_COLOR, rect)

    def update(self) -> None:
        """
        Redraws the screen.
        """
        self.screen.fill(DEAD_CELL_COLOR)

        v_draw_cell_rect = np.vectorize(self.draw_cell_rect)

        x = self.cell_grid.living_cell_coords
        if x.size:
            v_draw_cell_rect(x[:, 0], x[:, 1])
       
        pg.display.update()

    def on_mouse_button_down(self, event) -> None:
        """
        If the user left clicks, the cell under the mouse is revived.
        If the user right clicks, the cell under the mouse is killed.
        """
        button = event.button
        x, y = pg.mouse.get_pos()
        grid_x = floor(x/self.cell_width)
        grid_y = floor(y/self.cell_height)
        if button == pg.BUTTON_LEFT:
            self.cell_grid[grid_x, grid_y] |= 1
        elif button == pg.BUTTON_RIGHT:
            self.cell_grid[grid_x, grid_y] &= 0

        self.update()
    
    def on_key_down(self, event: pg.event) -> None:
        """
        Calls the function associated to the pressed key.
        """
        self.keybinds.get(event.key, lambda: None)()

        self.update()

    def before_loop(self) -> None:
        """
        Updates the display before the main_loop.
        """
        self.update()

    def on_loop(self) -> None:
        """
        Updates the cells if the game is updating cells every frame.
        """
        if self.updating:
            self.update_cells()
            self.update()
    