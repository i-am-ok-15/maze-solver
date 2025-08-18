import time
from tkinter import Tk, BOTH, Canvas


class Window:

    def __init__(self, width, height):
        self.root = Tk()
        self.root.title('Maze Solver')
        self.canvas = Canvas(self.root, width=width, height=height, bg="white")
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

    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win
    
    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

        if self.__win == None:
            return

        point_1 = Point(self.__x1, self.__y1)
        point_2 = Point(self.__x1, self.__y2)
        left_line = Line(point_1, point_2)
        if not self.has_left_wall:
            self.__win.draw_line(left_line, "white")
        else:
            self.__win.draw_line(left_line)

        point_1 = Point(self.__x2, self.__y1)
        point_2 = Point(self.__x2, self.__y2)
        right_line = Line(point_1, point_2)
        if not self.has_right_wall:
            self.__win.draw_line(right_line, "white")
        else:
            self.__win.draw_line(right_line)

        point_1 = Point(self.__x1, self.__y1)
        point_2 = Point(self.__x2, self.__y1)
        top_line = Line(point_1, point_2)
        if not self.has_top_wall:
            self.__win.draw_line(top_line, "white")
        else:
            self.__win.draw_line(top_line)

        point_1 = Point(self.__x1, self.__y2)
        point_2 = Point(self.__x2, self.__y2)
        bottom_line = Line(point_1, point_2)
        if not self.has_bottom_wall:
            self.__win.draw_line(bottom_line, "white")
        else:
            self.__win.draw_line(bottom_line)
        
        return self

    def draw_move(self, to_cell, undo=False):
        self.path_colour = "red"
        if undo:
            self.path_colour = "gray"
        
        path_point_1 = Point(self.__x1 + ((self.__x2 - self.__x1) / 2), (self.__y1 + (self.__y2 - self.__y1) / 2))
        path_point_2 = Point(to_cell.__x1 + ((to_cell.__x2 - to_cell.__x1) / 2), (to_cell.__y1 + (to_cell.__y2 - to_cell.__y1) / 2))

        path = Line(path_point_1, path_point_2)

        if self.__win != None:
            self.__win.draw_line(path, self.path_colour)


class Maze:

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []

        self.__create_cells()

    def __create_cells(self):

        if len(self.__cells) == 0:
            for col in range(self.__num_cols):
                col_list = []
                for row in range(self.__num_rows):
                    cell = Cell(self.__win)
                    col_list.append(cell)

                self.__cells.append(col_list)
    
        if self.__win != None:
            for col in range(self.__num_cols):
                for row in range(self.__num_rows):
                    self.__draw_cell(col, row)
    
    def __draw_cell(self, i, j):
        self.__x = ((self.__cell_size_x)* i + self.__x1)
        self.__y = ((self.__cell_size_y) * j + self.__y1)
        cell = self.__cells[i][j]

        if self.__win == None:
            return
        
        cell.draw(self.__x, 
                       self.__y, 
                       (self.__x + self.__cell_size_x), 
                       (self.__y + self.__cell_size_y)
                )


        self.__animate()

    def __animate(self):
        if self.__win == None:
            return
        
        Window.redraw(self.__win)
        time.sleep(0.001)

    def __break_entrance_and_exit(self):
        starter_cell = self.__cells[0][0]
        starter_cell.has_top_wall = False

        end_cell = self.__cells[-1][-1]
        end_cell.has_bottom_wall = False

        self.__draw_cell(0, 0)
        self.__draw_cell((self.__num_cols - 1), (self.__num_rows - 1))
   




        