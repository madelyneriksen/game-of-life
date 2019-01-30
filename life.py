"""Conway's game of life in a Python Dictionary.

The Game of Life is a staple in computer science, and was first
discovered by John Conway. The game assumes an infinite array for
cells, which is impossible to store in memory on a computer.
However, we can represent the sparse array with a Dictionary datatype, for
space efficiency using pure Python. This is in contrast to the common
Numpy array representations.
"""


import curses
import time


class Life(dict):
    """A Game of Life board, represented as a dictionary."""

    def __init__(self, *args, **kwargs):
        """Setting up our constructor."""
        super(Life, self).__init__(*args, **kwargs)

    def __missing__(self, *args, **kwargs):
        """An empty cell returns value zero.

        This is what lets us store a huge board and ignore dead cells.
        An Array based implementation would be very space intensive and
        expensive to iterate over."""
        return 0

    def check_cell(self, x: int, y: int):
        """check step for a cell. Determine if it lives or dies.

        Returns:
            live, dead: Two Lists of cells that live or die respectively.
        """
        x_coords = (x-1, x, x+1)
        y_coords = (y-1, y, y+1)
        total = 0

        # Sum up the value of all adjacent cells. You can easily speculate
        # neighbors from this total.
        for x_coord in x_coords:
            for y_coord in y_coords:
                total += self[x_coord, y_coord]

        # Creating the death and birth counts related to this cell.
        live, dead = [], []
        cell = self[x, y]
        if total == 3 and not cell:
            live.append((x, y))
        elif total < 3 or total > 4 and cell:
            dead.append((x, y))
        elif cell:
            pass
        return live, dead

    def queue_cells(self):
        """Get a list of all cells that need to be checked this transition.

        Rather than just calculating alive cells, we need to calculate values
        for their neighbors too, so life can spread. We also don't want to cycle
        through every cell in the world. The Game of Life is super sparse.
        """
        cells = []
        for x, y in self.keys():
            # Add all cell neighbors to the function.
            x_coords = (x-1, x, x+1)
            y_coords = (y-1, y, y+1)
            for x_coord in x_coords:
                for y_coord in y_coords:
                    cells.append((x_coord, y_coord))
        return cells

    def play_game(self):
        """Play one turn in the game of life."""
        live, dead = [], []
        # Create all the transitions for the turn
        for x, y in self.queue_cells():
            step_live, step_dead = self.check_cell(x, y)
            live += step_live
            dead += step_dead
        # Apply all transitions. Remember that in Life, the state of the board
        # doesn't change until every cell is accounted for.
        for x, y in dead:
            if self[x, y]:
                del self[x, y]
        for x, y in live:
            self[x, y] = 1


def loop(screen):
    """The main game loop.

    Curses is used to create a UI and visualization for the board. Because
    we can't fit an infinite board in a terminal, the player instead can
    move around with vim-keybinds (we're not savages).
    """
    # Initialize the board with an r-pentomino
    game = Life(
        {
            (25, 15): 1,
            (26, 15): 1,
            (25, 16): 1,
            (24, 16): 1,
            (25, 17): 1,
        }
    )
    adjust_x, adjust_y = 0, 0
    # Inputs set to be non-blocking.
    screen.nodelay(True)
    while True:
        move = screen.getch()
        if move == ord("h"):
            adjust_x += -1
        elif move == ord("l"):
            adjust_x += 1
        elif move == ord("k"):
            adjust_y += -1
        elif move == ord("j"):
            adjust_y += 1
        elif move == ord("q"):
            exit(0)
        else:
            pass
        screen.clear()
        game.play_game()
        max_y, max_x = screen.getmaxyx()
        for x, y in game.keys():
            visible_x = (0 + adjust_x) < x < (max_x + adjust_x)
            visible_y = (0 + adjust_y) < y < (max_y + adjust_y)
            if visible_x and visible_y:
                try:
                    screen.addstr(
                        y - adjust_y,
                        x - adjust_x,
                        "X"
                    )
                except curses.error:
                    pass
        curses.curs_set(0)
        screen.refresh()
        time.sleep(.1)


if __name__ == "__main__":
    try:
        curses.wrapper(loop)
    except KeyboardInterrupt:
        exit(0)
