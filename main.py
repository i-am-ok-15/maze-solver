from tkinter import Tk, BOTH, Canvas

from geometry import Window, Cell

def main():
    win_main = Window(800, 800)

    cell_1 = Cell(win_main).draw(100, 100, 200, 200)
    cell_2 = Cell(win_main).draw(200, 100, 300, 200)

    cell_1.draw_move(cell_2, undo=True)

    win_main.wait_for_close()

main()