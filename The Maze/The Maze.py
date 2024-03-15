import sys
from tkinter import Tk, Canvas, Event, PhotoImage
from tkinter.messagebox import showinfo

from utilities import *


class Game:
	def __init__(self) -> None:
		self.root = Tk()  # Main window
		self.canvas = Canvas(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)  # Canvas
		self.player = self.canvas.create_rectangle(  # Player
			PLAYER_POSITION.x1 * TILE + 1, PLAYER_POSITION.y1 * TILE + 1,
			PLAYER_POSITION.x2 * TILE - 1, PLAYER_POSITION.y2 * TILE - 1,
			fill=RED, outline=RED
		)

		# Game elements lists
		self.void: Cells = []
		self.walls: Cells = []
		self.coins: Cells = []
		self.doors: Cells = []
		self.exits: Cells = []

		# Total coins that player got during the game
		self.total_coins = 0

		# Music
		pygame.init()
		pygame.mixer.init()

	def __repr__(self) -> str:
		return f'Player: 1, Walls: {len(self.walls)}, Coins: {len(self.coins)}, Doors: {len(self.doors)}, Exits: {len(self.exits)}, Void: {len(self.void)}'

	def setup_window(self) -> None:
		# Basic window setup
		self.root.title(WINDOW_TITLE)
		self.root.resizable(WINDOW_RESIZABLE, WINDOW_RESIZABLE)
		self.root['background'] = WHITE
		self.root.tk.call('wm', 'iconphoto', self.root, PhotoImage(file=WINDOW_ICON))

		# Pack canvas
		self.canvas.pack()

	def setup_canvas(self) -> None:
		# Go throw the GRID and append all the game elements to lists and draw them on canvas
		for y, row in enumerate(GRID):
			for x, cell in enumerate(row):
				match cell:
					case CellType.VOID.value:
						self.void.append(Cell(x, y, x + 1, y + 1))
					case CellType.WALL.value:
						wall_id: int = self.canvas.create_rectangle(x * TILE, y * TILE,
						                                            x * TILE + TILE,
						                                            y * TILE + TILE, fill=BLACK,
						                                            outline=BLACK)
						self.walls.append(Cell(x, y, x + 1, y + 1, object_id=wall_id))
					case CellType.COIN.value:
						coin_id: int = self.canvas.create_rectangle(x * TILE + 3, y * TILE + 3,
						                                            x * TILE + TILE - 3,
						                                            y * TILE + TILE - 3, fill=YELLOW,
						                                            outline=YELLOW)
						self.coins.append(Cell(x, y, x + 1, y + 1, object_id=coin_id))
					case CellType.DOOR.value:
						door_id: int = self.canvas.create_rectangle(x * TILE + 1, y * TILE + 1,
						                                            x * TILE + TILE - 1,
						                                            y * TILE + TILE - 1, fill=BLUE,
						                                            outline=BLUE)
						self.doors.append(Cell(x, y, x + 1, y + 1, object_id=door_id))
					case CellType.EXIT.value:
						exit_id: int = self.canvas.create_rectangle(x * TILE + 1, y * TILE + 1,
						                                            x * TILE + TILE - 1,
						                                            y * TILE + TILE - 1, fill=GREEN,
						                                            outline=GREEN)
						self.exits.append(Cell(x, y, x + 1, y + 1, object_id=exit_id))

	def move(self, event: Event) -> None:
		# Get player input
		x = y = 0.0

		# Process player input and move the player in that direction
		match event.keysym.lower():
			case 'left':
				x = -TILE
			case 'right':
				x = TILE
			case 'up':
				y = -TILE
			case 'down':
				y = TILE

		# Multiply the speed
		x *= PLAYER_SPEED_MULTIPLIER
		y *= PLAYER_SPEED_MULTIPLIER

		# Move and check collision with game elements
		self.canvas.move(self.player, x, y)
		self.check_collision(x, y)

	def check_collision(self, x: float, y: float) -> None:
		# Check for collisions with walls
		for wall in self.walls:
			if self.player in self.canvas.find_overlapping(wall.x1 * TILE, wall.y1 * TILE,
			                                               wall.x2 * TILE, wall.y2 * TILE):
				self.canvas.move(self.player, -x, -y)
				return

		# Check for collisions with coins
		for coin in self.coins:
			if self.player in self.canvas.find_overlapping(coin.x1 * TILE, coin.y1 * TILE,
			                                               coin.x2 * TILE, coin.y2 * TILE):
				self.total_coins += 1
				logging.info(f"You have {self.total_coins} coin{'s' if self.total_coins > 1 else ''}.")

				self.coins.remove(coin)
				self.canvas.delete(coin.object_id)

				# Remove all doors if you have all the coins
				if self.total_coins == MAX_COINS:
					play(DOOR_OPEN_SOUND)

					for door in self.doors:
						self.doors.remove(door)
						self.canvas.delete(door.object_id)
				else:
					play(COIN_SOUND)

				return

		# Check for collisions with doors
		for door in self.doors:
			if self.player in self.canvas.find_overlapping(door.x1 * TILE, door.y1 * TILE,
			                                               door.x2 * TILE, door.y2 * TILE):
				if self.total_coins < MAX_COINS:
					self.canvas.move(self.player, -x, -y)

				return

		# Check for collisions with exits
		for exit_ in self.exits:
			if self.player in self.canvas.find_overlapping(exit_.x1 * TILE, exit_.y1 * TILE,
			                                               exit_.x2 * TILE, exit_.y2 * TILE):
				self.win()

	@staticmethod
	def win() -> None:
		# Display the win screen and exit the game
		play(END_SOUND)
		showinfo('Congratulations!', 'You have successfully completed the game!')
		pygame.quit()
		sys.exit(0)

	def bind_events(self) -> None:
		# Bind all key events
		self.canvas.bind_all('<Key>', self.move)
		self.canvas.bind_all('<Escape>', lambda event: sys.exit(0))

	def run(self) -> None:
		# Setup
		self.setup_window()
		self.setup_canvas()
		self.bind_events()

		# Debug
		logging.debug(repr(self))
		logging.info(f'You have no coins.')

		# Run
		play(BACKGROUND_MUSIC)
		self.root.mainloop()


# Main entry point
def main() -> None:
	game: Game = Game()
	game.run()


if __name__ == '__main__':
	main()
