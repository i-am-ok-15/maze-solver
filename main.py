from tkinter import Tk, BOTH, Canvas

class Window:

    def __init__(self, width, height):
        self.root = Tk()
        self.width = width
        self.height = height
        self.root.title('Maze Solver')
        self.canvas = Canvas(self.root, width=width - 10, height=height - 10)
        self.canvas.pack()
        self.window_running = False
        self.root.protocol('WM_DELETE_WINDOW', self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.window_running = True
        while self.window_running:
            self.redraw()
    
    def close(self):
        self.window_running = False

def main():
    win = Window(800, 600)
    win.wait_for_close()

main()