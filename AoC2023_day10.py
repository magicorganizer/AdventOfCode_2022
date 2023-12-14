import logging

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
        self.curr_point = self.start
        self.matrix_ref = matrix_ref
        self.path1 = [self.start]
        self.search_path()

    def search_path(self):
        loop_complete = False
        while not loop_complete:
            for neigbor_pos in self.curr_point.get_compatible_neighbors():
                if self.is_point_new(self.path1, neigbor_pos):
                    self.curr_point = Point(neigbor_pos, self.matrix_ref)
                    self.path1.append(self.curr_point)
                    print(self.curr_point.pos, self.curr_point.char)
                    # abbruchkriterium fehlt
                    # bei S zwei pfade
                    # jeden pfad einzeln berechnen

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
    DEBUG = True

    def __init__(self):
        self.commands = self.load_puzzle_input()
        self.grid = Matrix(self.commands)
        self.grid.print_matrix()
        self.grid_of_points = list()
        self.create_point_matrix()
        self.path = Path(self.find_start(), self.grid)
        self.answer = 0
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
