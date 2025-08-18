from tkinter import Tk, BOTH, Canvas

from geometry import Window, Cell

def main():
    win = Window(800, 800)

    cell_1 = Cell(win).draw(50, 50, 100, 100)

    win.wait_for_close()

main()