"""
This is a legacy code of this game from 2019-2020 (I don't remember). And I made an improved version of it.

I was very young then and I knew a bit of Python.
I didn't know what "Clean Code" or "Type Annotations" are, so this code absolutely suck in very single way.
I didn't know English well, so I named "coins" -> "coints", lol.
I made LOTS of mistakes and bad practices.

In 2024, I learned Dataclasses, NumPy, logging, OOP, Pygame, type annotations and many more.

P.S. This doc-string was written in 2024. But the code below has 0 changes.
"""

from tkinter import *
from tkinter import messagebox
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                 WWWWWW    KW",
    "WWWWWWWWWWW  WWW  WWWWWW  W  W",
    "WWWWWWW      WWW  WWWWWW  W  W",
    "WWWWWWW  WWWWWWW          W  W",
    "W        WWW      WWWWWW  W  W",
    "W  WWWW  WWW  WWWWWWWW    W  W",
    "W  WWWW  WWW       WWW  WWW  W",
    "W     W    WWWWWW  WWW  W    W",
    "WWWW  WWW  WWWWWW    W  W  WWW",
    "WW            WWWWW  W  W    W",
    "WW  WWWWWWW   WWW       WWW  W",
    "WW    W                KWWW  W",
    "WWWW  W       WWWWWWWWWWW    W",
    "WW    WWWWWWWWWWWWWWWWWWW    W",
    "WW    W                     KW",
    "WWBW  W WWWWWWWWW  WWWW   WWWW",
    "WW  WWW       KWWWW      WWWWW",
    "WWEEWWWWWWWWWWWWWWWWWWWWWWWWWW",
]
x = 0
y = 0
walls = list()
exits = list()
doors = list()
coints = list()
co = 0
tk = Tk()
tk["bg"] = "white"
def player_move(event):
    global co
    dx = dy = 0
    key = event.keysym
    if key == "Up":
        dy = -16
    elif key == "Down":
        dy = 16
    elif key == "Left":
        dx = -16
    elif key == "Right":
        dx = 16
    canvas.move(player, dx, dy)
    for wall in walls:
        if player in canvas.find_overlapping(wall[0], wall[1], wall[2], wall[3]):
            canvas.move(player, -dx, -dy)
    for exit in exits:
        if player in canvas.find_overlapping(exit[0], exit[1], exit[2], exit[3]):
            messagebox.showinfo("WIN", "You WIN!")
            tk.destroy()
    for coint in coints:
        if player in canvas.find_overlapping(coint[0], coint[1], coint[2], coint[3]):
            co += 1
            coints.remove(coint)
            canvas.create_rectangle(coint[0], coint[1], coint[2], coint[3], fill="white", outline="white")
    for door in doors:
        if player in canvas.find_overlapping(door[0], door[1], door[2], door[3]):
            if co < 4:
                canvas.move(player, -dx, -dy)
            else:
                doors.remove(door)
                canvas.create_rectangle(door[0], door[1], door[2], door[3], fill="white", outline="white")
canvas = Canvas(width=480, height=304)
canvas.pack()
player = canvas.create_rectangle(17, 17, 31, 31, fill="red")
for i in level:
    for j in i:
        if j == "W":
            canvas.create_rectangle(x, y, x+16, y+16, fill="black")
            walls.append((x, y, x+16, y+16))
        if j == "E":
            canvas.create_rectangle(x, y, x+16, y+16, fill="green", outline="black")
            exits.append((x, y, x+16, y+16))
        if j == "B":
            canvas.create_rectangle(x, y, x+16, y+16, fill="blue", outline="black")
            doors.append((x, y, x+16, y+16))
        if j == "K":
            canvas.create_rectangle(x, y, x+16, y+16, fill="yellow", outline="black")
            coints.append((x, y, x+16, y+16))
        x += 16
    y += 16
    x = 0
canvas.bind_all("<Key>", player_move)
tk.title("Level")
tk.resizable(0, 0)
tk.attributes("-topmost", 1)
if __name__ == '__main__':
    tk.mainloop()