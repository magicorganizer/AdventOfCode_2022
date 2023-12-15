import logging
import numpy as np
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.INFO, filename='AoC2023.log', filemode='w')

class Point:
    def __init__(self, tupel_pos, matrix_ref):
        self.pos = tupel_pos
        self.matrix_ref = matrix_ref
        self.distance_from_start = None
        self.char = self.matrix_ref.get_element_xy(*self.pos)

    def get_compatible_neighbors(self):
        list_of_compatible_neighbors = list()
        # get all neighbors
        pos_x = self.pos[0]
        pos_y = self.pos[1]
        # brauchen nur up, down, left , right
        #neighbors = [(x, y) for x in range(pos_x - 1, pos_x + 2) for y in range(pos_y - 1, pos_y + 2)]
        neighbors = { "up": (pos_x, pos_y - 1),
                      "down": (pos_x, pos_y + 1),
                      "left": (pos_x - 1, pos_y),
                      "right": (pos_x + 1, pos_y)
                      }
        possible_directions = self.get_possible_directions()
        for possible_fitting in possible_directions:
            neighbor = neighbors[possible_fitting]
            neighbor_char =self.matrix_ref.get_element_xy(*neighbor)
            if self.get_possible_fitting(neighbor_char, possible_fitting):
                list_of_compatible_neighbors.append(neighbor)
        return list_of_compatible_neighbors


    def get_possible_directions(self):
        dict_lookup = {"S": ["up", "down", "left", "right"],
                       "|": ["up", "down"],
                       "-": ["left", "right"],
                       "L": ["up", "right"],
                       "J": ["up", "left"],
                       "7": ["down", "left"],
                       "F": ["down", "right"],
                       ".": [],
                       }
        return dict_lookup[self.char]

    def get_possible_fitting(self, neighbor_char, direction):
        dict_fitting_lookup = {"S": {"up": True, "down": True, "left": True, "right": True},
                               "|": {"up": True, "down": True},
                               "-": {"left": True, "right": True},
                               "L": {"down": True, "left": True},
                               "J": {"down": True, "right": True},
                               "7": {"up": True, "right": True},
                               "F": {"up": True, "right": True},
                               ".": {},
                               }
        try:
            retval = dict_fitting_lookup[neighbor_char][direction]
        except KeyError:
            retval = False
        return retval


class Path:
    def __init__(self, tupel_start, matrix_ref):
        self.start = Point(tupel_start, matrix_ref)
        self.curr_point1 = self.start
        self.curr_point2 = self.start
        self.matrix_ref = matrix_ref
        self.path1 = [self.start]
        self.path2 = [self.start]
        self.split_path()
        boTrack1 = True
        boTrack2 = True
        while boTrack1 and boTrack2:
            boTrack1 = self.follow_path(self.path1)
            boTrack2 = self.follow_path(self.path2)
        print(f"done {len(self.path1)}/{len(self.path2)}")
        self.answer = max(len(self.path1), len(self.path2)) - 1
        pass

    def follow_path(self, path):
        curr_point = path[-1]
        for neigbor_pos in curr_point.get_compatible_neighbors():
            if (self.is_point_new(self.path1, neigbor_pos) and
                    self.is_point_new(self.path2, neigbor_pos)):
                curr_point = Point(neigbor_pos, self.matrix_ref)
                path.append(curr_point)
                print(curr_point.pos, curr_point.char)
                return True
        return False

    def search_path(self):
        loop_complete = False
        while not loop_complete:
            found_new_point = False
            for neigbor_pos in self.curr_point1.get_compatible_neighbors():
                if self.is_point_new(self.path1, neigbor_pos):
                    self.curr_point = Point(neigbor_pos, self.matrix_ref)
                    self.path1.append(self.curr_point1)
                    print(self.curr_point1.pos, self.curr_point1.char)
                    found_new_point = True

                    # bei S zwei pfade
                    # jeden pfad einzeln berechnen
            loop_complete = not found_new_point

    def split_path(self):
        list_neighbors = self.curr_point1.get_compatible_neighbors()
        if self.is_point_new(self.path1, list_neighbors[0]):
            self.curr_point1 = Point(list_neighbors[0], self.matrix_ref)
            self.path1.append(self.curr_point1)
            print("path1 ", self.curr_point1.pos, self.curr_point1.char)
        if self.is_point_new(self.path2, list_neighbors[1]):
            self.curr_point2 = Point(list_neighbors[1], self.matrix_ref)
            self.path2.append(self.curr_point2)
            print("path2 ",self.curr_point2.pos, self.curr_point2.char)


    def is_point_new(self, list_path, tupel_pos):
        for point in list_path:
            if point.pos == tupel_pos:
                return False
        return True

class Matrix:
    def __init__(self, list_lines):
        self.matrix = []
        self.max_x = 0
        self.max_y = 0

        for line in list_lines:
            if line:
                self.matrix.append([*line])
                self.max_y += 1
                self.max_x = len(line) if len(line) > self.max_x else self.max_x

    def print_matrix(self):
        for matrix_row in self.matrix:
            print(matrix_row)

    def get_element_xy(self, x, y):
        if x in range(0, self.max_x) and y in range(0, self.max_y):
            return self.matrix[y][x]
        else:
            return None

    def set_element_xy(self, x, y, char):
        self.matrix[y][x] = char

class AoC2023_Day10:
    DEBUG = False

    def __init__(self):
        self.commands = self.load_puzzle_input()
        self.grid = Matrix(self.commands)
        self.grid.print_matrix()
        self.grid_of_points = list()
        self.create_point_matrix()
        self.path = Path(self.find_start(), self.grid)
        self.answer = self.path.answer
        self.answer2 = 0

    def load_puzzle_input(self):
        commands = list()
        if AoC2023_Day10.DEBUG:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day10.dbg"
        else:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day10.txt"
        with open(filename) as file:
            for console_output in file:
                commands.append(console_output.rstrip())

        return commands

    def find_start(self):
        for y in range(self.grid.max_y):
            for x in range(self.grid.max_x):
                if self.grid.get_element_xy(x, y) == "S":
                    return x, y
        return None

    def find_start(self):
        for y in range(self.grid.max_y):
            for x in range(self.grid.max_x):
                if self.grid.get_element_xy(x, y) == "S":
                    return x, y

    def create_point_matrix(self):
        row_list = list()
        for y in range(self.grid.max_y):
            for x in range(self.grid.max_x):
                row_list.append(Point((x, y), self.grid))
            self.grid_of_points.append(row_list)

    def run_AoC(self):
        for line in self.commands:
            pass

    def run_AoC_part2(self):
        pass

puzzle = AoC2023_Day10()
puzzle.run_AoC()
print(f"done! answer= {puzzle.answer}")
puzzle.run_AoC_part2()
print(f"done! answer2= {puzzle.answer2}")

data = [(2, 2), (3, 2), (4, 1), (4, 0), (3, 0), (3, 1), (4, 2),
        (4, 3), (4, 4), (3, 3), (3, 4), (2, 4), (2, 3), (1, 4),
        (0, 4), (0, 3), (1, 3), (0, 2), (1, 2), (0, 1), (0, 0),
        (1, 0), (1, 1), (2, 0), (2, 1)]
data = puzzle.path.path1
for i in range(len(data) -1):
  x1 = data[i].pos[0]
  y1 = data[i].pos[1]
  x2 = data[i+1].pos[0]
  y2 = data[i+1].pos[1]
  plt.plot([x1, x2], [y1, y2], c='blue')
  plt.scatter(x1, y1, c='blue')

data = puzzle.path.path2
for i in range(len(data) -1):
  x1 = data[i].pos[0]
  y1 = data[i].pos[1]
  x2 = data[i+1].pos[0]
  y2 = data[i+1].pos[1]
  plt.plot([x1, x2], [y1, y2], c='red')
  plt.scatter(x1, y1, c='red')
plt.show()