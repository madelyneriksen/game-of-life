Conway's Game of Life
=======

_Life_ implemented in pure Python3, visualized with curses and kept on a sparse matrix.

## Getting Started

You will need to have Python3 installed on your system with `curses` support. There are no additional dependencies!

Clone the project and start a game with the following commands:

```bash
git clone https://github.com/madelyneriksen/game-of-life life
cd life
python3 life.py
```

Move around on the board with `hjkl`. You can close the game by pressing either `q` or `C-c`!

## How It Works

Rather than representing the board with a matrix, numpy array, or Python `list`, we're using a dictionary. In mathematics, a representation of a sparse matrix with a dictionary is called a _dictionary of keys_, where all absent values are assumed to be zero.

Live cells are stored under their `(x, y)` coordinates:

```python
{
    (10, 11): 1,
}
```

Curses then only renders cells that are on the visible screen.

## License

All code in this project is MIT Licensed.
