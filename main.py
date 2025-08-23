from tkinter import Tk, BOTH, Canvas

from geometry import * # Window, Cell, Maze

def main():
    win_main = Window(900, 900)

    maze_1 = Maze(20, 20, 20, 20, 40, 40, win_main, 1)
    maze_1._Maze__break_entrance_and_exit()
    maze_1._Maze__break_wall_r(0, 0)
    maze_1._Maze__reset_cells_visited()

    win_main.wait_for_close()

main()