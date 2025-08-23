import time, random
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
            width=3
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
        self.visited = False
    
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

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, rand_seed = None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.rand_seed = rand_seed

        if self.rand_seed != None:
            self.rand_seed = random.seed(rand_seed)

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
        time.sleep(0.00001)

    def __break_entrance_and_exit(self):
        starter_cell = self.__cells[0][0]
        starter_cell.has_top_wall = False

        end_cell = self.__cells[-1][-1]
        end_cell.has_bottom_wall = False

        self.__draw_cell(0, 0)
        self.__draw_cell((self.__num_cols - 1), (self.__num_rows - 1))
    
    def __break_wall_r(self, i, j):

        starting_cell = self.__cells[i][j]
        starting_cell.visited = True

        while True:

            possible_next_cells = []

            if j > 0 and not self.__cells[i][j - 1].visited: #check above
                possible_next_cells.append((i, j - 1))
            
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited: #check right
                possible_next_cells.append((i + 1, j))
            
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited: #check below
                possible_next_cells.append((i, j + 1))

            if i > 0 and not self.__cells[i - 1][j].visited: #check left
                possible_next_cells.append((i - 1, j))
            
            if len(possible_next_cells) == 0:
                self.__draw_cell(i, j)
                return

            next_cell = random.choice(possible_next_cells)
            next_i, next_j = next_cell

            if next_i == i and next_j == j - 1:
                #next cell is above, break current cell top and next cell bottom
                self.__cells[i][j].has_top_wall = False
                self.__cells[next_i][next_j].has_bottom_wall = False
            elif next_i == i + 1 and next_j == j:
                #next cell is right
                self.__cells[i][j].has_right_wall = False
                self.__cells[next_i][next_j].has_left_wall = False
            elif next_i == i and next_j == j + 1:
                #next cell is below
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[next_i][next_j].has_top_wall = False
            elif next_i == i - 1 and next_j == j:
                #next cell is left         
                self.__cells[i][j].has_left_wall = False
                self.__cells[next_i][next_j].has_right_wall = False
   
            self.__break_wall_r(next_i, next_j)
    
    def __reset_cells_visited(self):

        for col in self.__cells:
            for cell in col:
                cell.visited = False
    
    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):

        current_cell = self.__cells[i][j]

        self.__animate()
        current_cell.visited = True

        if current_cell == self.__cells[-1][-1]:
            return True


        if j > 0 and not self.__cells[i][j - 1].visited: #check above
            if not current_cell.has_top_wall:
                if not self.__cells[i][j - 1].has_bottom_wall:
                    current_cell.draw_move(self.__cells[i][j - 1])
                    if self._solve_r(i, j - 1):
                        return True
                    current_cell.draw_move(self.__cells[i][j - 1], undo=True)  

        if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited: #check right
            if not current_cell.has_right_wall:
                if not self.__cells[i + 1][j].has_left_wall:
                    current_cell.draw_move(self.__cells[i + 1][j])
                    if self._solve_r(i + 1, j):
                        return True
                    current_cell.draw_move(self.__cells[i + 1][j], undo=True)  

        if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited: #check below
            if not current_cell.has_bottom_wall:
                if not self.__cells[i][j + 1].has_top_wall:
                    current_cell.draw_move(self.__cells[i][j + 1])
                    if self._solve_r(i, j + 1):
                        return True
                    current_cell.draw_move(self.__cells[i][j + 1], undo=True)  

        if i > 0 and not self.__cells[i - 1][j].visited: #check left
            if not current_cell.has_left_wall:
                if not self.__cells[i - 1][j].has_right_wall:
                    current_cell.draw_move(self.__cells[i - 1][j])
                    if self._solve_r(i - 1, j):
                        return True
                    current_cell.draw_move(self.__cells[i - 1][j], undo=True)                

        else:
            return False



        