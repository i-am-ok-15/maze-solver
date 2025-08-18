from tkinter import Tk, BOTH, Canvas

from geometry import Window, Cell, Maze

def main():
    win_main = Window(800, 800)

    # cell_1 = Cell(win_main).draw(20, 20, 40, 40)
    # cell_2 = Cell(win_main).draw(40, 20, 60, 40)

    # cell_1.draw_move(cell_2, undo=True)

    maze_1 = Maze(20, 20, 50, 50, 15, 15, win_main)


    win_main.wait_for_close()

main()