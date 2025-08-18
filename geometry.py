from tkinter import Tk, BOTH, Canvas

class Window:

    def __init__(self, width, height):
        self.root = Tk()
        self.root.title('Maze Solver')
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=1)
        self.window_running = False
        self.root.protocol('WM_DELETE_WINDOW', self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.window_running = True
        while self.window_running:
            self.redraw()
        print("window closed...")
    
    def close(self):
        self.window_running = False
    
    def draw_line(self, Line, fill_colour='black'):
        Line.draw(self.canvas, fill_colour)


class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:

    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, Canvas, fill_colour):
        Canvas.create_line(
            self.point_1.x, 
            self.point_1.y, 
            self.point_2.x, 
            self.point_2.y, 
            fill=fill_colour, 
            width=2
        )


class Cell:

    def __init__(self, Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = Window
    
    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

        if self.has_left_wall:
            point_1 = Point(self.__x1, self.__y1)
            point_2 = Point(self.__x1, self.__y2)
            left_line = Line(point_1, point_2)
            self.__win.draw_line(left_line)

        if self.has_right_wall:
            point_1 = Point(self.__x2, self.__y1)
            point_2 = Point(self.__x2, self.__y2)
            left_line = Line(point_1, point_2)
            self.__win.draw_line(left_line)

        if self.has_top_wall:
            point_1 = Point(self.__x1, self.__y1)
            point_2 = Point(self.__x2, self.__y1)
            left_line = Line(point_1, point_2)
            self.__win.draw_line(left_line)

        if self.has_bottom_wall:
            point_1 = Point(self.__x1, self.__y2)
            point_2 = Point(self.__x2, self.__y2)
            left_line = Line(point_1, point_2)
            self.__win.draw_line(left_line)
        
        return self

    def draw_move(self, to_cell, undo=False):
        self.path_colour = "red"
        if undo:
            self.path_colour = "gray"
        
        path_point_1 = Point(self.__x1 + ((self.__x2 - self.__x1) / 2), (self.__y1 + (self.__y2 - self.__y1) / 2))
        path_point_2 = Point(to_cell.__x1 + ((to_cell.__x2 - to_cell.__x1) / 2), (to_cell.__y1 + (to_cell.__y2 - to_cell.__y1) / 2))

        path = Line(path_point_1, path_point_2)

        self.__win.draw_line(path, self.path_colour)



