from typing import Union

import numpy as np
import numpy.typing as npt


class CellGrid:
    """
    A grid of cells.
    """
    __slots__ = "cells", "width", "height", "cell_neighbors"
    
    def __init__(self, width: int, height: int) -> None:
        """
        Creates a `width`x`height` grid of cells (booleans).
        """
        window = np.full((width+2, height+2), False)
        self.cells = window[1:-1, 1:-1]
        self.cell_neighbors = np.lib.stride_tricks.sliding_window_view(window, (3, 3))
        self.width = width
        self.height = height
        
    def randomize(self, odds=2) -> None:
        """
        Sets the grid to a random configuration.
        The odds of a cell being alive are 1/`odds`.
        """
        c = [*[False]*(odds-1), True]
        r = np.random.choice(c, self.cells.shape)
        self.cells &= r
        self.cells |= r
    
    def clear(self) -> None:
        """
        Kills all the cells in the grid.
        """
        r = np.zeros(self.cells.shape, dtype="b1")
        self.cells &= r

    @property
    def living_cell_coords(self) -> npt.NDArray[np.bool8]:
        """
        Returns the coordinates of all the living cells.
        """
        return np.transpose(self.cells.nonzero())

    def __getitem__(self, key) -> Union[np.bool8, npt.NDArray[np.bool8]]:
        return self.cells[key]

    def __setitem__(self, key, value) -> None:
        self.cells[key] = value

    def __delitem__(self, key) -> None:
        del(self.cells[key])
