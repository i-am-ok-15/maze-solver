from tkinter import Tk, BOTH, Canvas

from geometry import Window, Cell, Maze

def main():
    win_main = Window(800, 800)

    maze_1 = Maze(20, 20, 50, 50, 15, 15, win_main)

    win_main.wait_for_close()

main()