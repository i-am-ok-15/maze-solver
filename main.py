from tkinter import Tk, BOTH, Canvas

from geometry import * # Window, Cell, Maze

def main():
    win_main = Window(800, 800)

    maze_1 = Maze(20, 20, 4, 4, 15, 15, win_main)
    maze_1._Maze__break_entrance_and_exit()

    win_main.wait_for_close()

main()