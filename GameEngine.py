

import enum
import math
import random


class State(enum.Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class GameEngine:
    grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    score = 0
    ROWS = 4
    COLS = 4

    def __init__(self):
        self.reset()

    @staticmethod
    def _slide_left(line):
        """Slide tiles left, merge equal neighbors once, pad with zeros.
        Returns (new_line, points_earned)."""
        tiles = [v for v in line if v != 0]
        merged = []
        points = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                value = tiles[i] * 2
                merged.append(value)
                points += value
                i += 2  # skip the tile we just merged in
            else:
                merged.append(tiles[i])
                i += 1
        merged += [0] * (len(line) - len(merged))
        return merged, points

    def shift(self, state: State):
        vertical = state in (State.UP, State.DOWN)
        reverse = state in (State.RIGHT, State.DOWN)

        # Transpose for vertical moves so columns become rows
        grid = [list(c) for c in zip(*self.grid)] if vertical else self.grid

        new_grid = []
        for line in grid:
            if reverse:
                line = line[::-1]
            slid, points = self._slide_left(line)
            if reverse:
                slid = slid[::-1]
            self.score += points
            new_grid.append(slid)

        # Transpose back
        if vertical:
            new_grid = [list(r) for r in zip(*new_grid)]

        moved = new_grid != self.grid
        self.grid = new_grid
        self.place_new_item()
        return moved

    def place_new_item(self):
        spots = 1
        available_spots = []
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col] == 0:
                    available_spots.append((row,col))
        if len(available_spots) == 0:
            self.game_over = True
        
        for i in range(spots):
            rand_spot = random.randint(0, len(available_spots)-1)
            x, y = available_spots[rand_spot]
            self.grid[x][y] = random.randint(1,2) * 2
        
        self.game_over = False

    def reset(self):
        self.grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        spots = 3

        for i in range(spots):
            x = random.randint(0, self.COLS-1)
            y = random.randint(0, self.ROWS-1)
            self.grid[x][y] = random.randint(1, 2) * 2

    def get_grid_val(self, row, col):
        return self.grid[row][col]

    def did_lose(self) -> bool:
        for row in self.ROWS:
            for col in self.COLS:
                if self.grid[row][col] == 0:
                    return False

        return True
