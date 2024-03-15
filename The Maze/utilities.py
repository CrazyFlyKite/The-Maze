# Hide the pygame support prompt
from contextlib import redirect_stdout

with redirect_stdout(None):
	import pygame

from dataclasses import dataclass
from enum import Enum
import logging
from os import PathLike
from typing import List, Optional, Final, TypeAlias

import numpy as np

from setup_logging import setup_logging

# Setup logging
setup_logging(level=logging.DEBUG, logging_format='[%(levelname)s] - %(message)s')

# Custom types
PathLikeString: TypeAlias = str | bytes | PathLike


# Level Grid
def get_grid(grid_file: PathLikeString, separator: Optional[str] = ' ') -> np.ndarray:
	try:
		with open(grid_file, 'r', encoding='utf-8') as file:
			return np.array([[int(number) for number in line.strip().split(separator)] for line in file.readlines()])
	except OSError:
		return np.zeros(shape=(1, 1))


GRID: Final[np.ndarray] = get_grid('../assets/data/grid.txt')
GRID_HEIGHT, GRID_WIDTH = GRID.shape


# Cell types
class CellType(Enum):
	VOID: Final[int] = 0
	WALL: Final[int] = 1
	COIN: Final[int] = 2
	DOOR: Final[int] = 3
	EXIT: Final[int] = 4


# Other
TILE: Final[int] = 16
MAX_COINS: Final[int] = np.count_nonzero(GRID == CellType.COIN)

# Window
WINDOW_TITLE: Final[str] = 'The Maze'
WINDOW_WIDTH: Final[int] = GRID_WIDTH * TILE
WINDOW_HEIGHT: Final[int] = GRID_HEIGHT * TILE
WINDOW_RESIZABLE: Final[bool] = False
WINDOW_ICON: Final[PathLikeString] = '../assets/images/icon.png'

# Colors
BLACK: Final[str] = 'black'
WHITE: Final[str] = 'white'
RED: Final[str] = 'red'
YELLOW: Final[str] = 'yellow'
GREEN: Final[str] = 'green'
BLUE: Final[str] = 'blue'


# Cell
@dataclass(frozen=True)
class Cell:
	x1: int
	y1: int
	x2: int
	y2: int
	object_id: int = 0


Cells: TypeAlias = List[Cell]

# Player
PLAYER_POSITION: Final[Cell] = Cell(1, 1, 2, 2)
PLAYER_SPEED_MULTIPLIER: Final[float] = 1.0


# Music
@dataclass(frozen=True)
class SoundEffect:
	name: PathLikeString
	volume: float = 0.2
	loops: int = 0


def play(sound_effect: SoundEffect) -> None:
	sound: pygame.mixer.Sound = pygame.mixer.Sound(sound_effect.name)
	sound.set_volume(sound_effect.volume)
	sound.play(sound_effect.loops)


BACKGROUND_MUSIC: Final[SoundEffect] = SoundEffect('../assets/music/sneaky-snitch.mp3', loops=-1)
COIN_SOUND: Final[SoundEffect] = SoundEffect('../assets/music/coin.mp3', 0.1)
DOOR_OPEN_SOUND: Final[SoundEffect] = SoundEffect('../assets/music/door-open.mp3', 0.1)
END_SOUND: Final[SoundEffect] = SoundEffect('../assets/music/end.mp3', 0.1)
