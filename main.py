from tkinter import Tk, BOTH, Canvas

from geometry import * # Window, Cell, Maze

def main():
    win_main = Window(1000, 1000)

    maze_1 = Maze(20, 20, 40, 40, 20, 20, win_main)
    maze_1._Maze__break_entrance_and_exit()
    maze_1._Maze__break_wall_r(0, 0)
    maze_1._Maze__reset_cells_visited()
    maze_1.solve()

    win_main.wait_for_close()

main()