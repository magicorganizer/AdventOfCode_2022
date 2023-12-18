import logging
from itertools import permutations, combinations
import numpy as np
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.INFO, filename='AoC2023.log', filemode='w')


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
        for row_idx, matrix_row in enumerate(self.matrix):
            print(f"{row_idx}: {matrix_row}")
        pass

    def get_element_xy(self, x, y):
        if x in range(0, self.max_x) and y in range(0, self.max_y):
            return self.matrix[y][x]
        else:
            return None

    def set_element_xy(self, x, y, char):
        self.matrix[y][x] = char

class Universe(Matrix):

    def __init__(self, list_of_lines):
        super().__init__(list_of_lines)
        self.list_of_galaxies = list()
        self.expand_universe()
        self.get_all_galaxies()
        self.list_of_galaxy_combinations = self.get_galaxy_combinations(self.list_of_galaxies)
        self.answer = self.get_sum_of_galaxy_distances()
        pass

    def get_all_galaxies(self):
        for col_idx in range(self.max_x + 1):
            for row_idx in range(self.max_y + 1):
                if "#" == self.get_element_xy(col_idx, row_idx):
                    self.list_of_galaxies.append((col_idx, row_idx ))

    def get_row_by_index(self, row_idx):
        return self.matrix[row_idx]

    def get_col_by_index(self, col_idx):
        return [self.matrix[row_idx][col_idx] for row_idx in range(self.max_y)]

    def insert_empty_row(self, row_idx):
        self.matrix.insert(row_idx, ["." for row_idx in range(self.max_x)])
        self.max_y = len(self.matrix)

    def insert_empty_col(self, col_idx):
        for row_idx in range(self.max_y):
            self.matrix[row_idx].insert(col_idx, ".")
        self.max_x = len(self.matrix[0])
        self.print_matrix()
        pass

    def expand_universe(self):
        """every row and comumn of the universe, that contains no galaxy will be expanded by adding
         an empty row or an empty col"""
        list_of_empty_rows = list()
        for row_idx in range(self.max_y):
            if "#" not in self.get_row_by_index(row_idx):
                list_of_empty_rows.append(row_idx)

        list_of_empty_cols = list()
        for col_idx in range(self.max_x):
            if "#" not in self.get_col_by_index(col_idx):
                list_of_empty_cols.append(col_idx)

        # backwads to do not affect the index
        for row_idx in reversed(list_of_empty_rows):
            self.insert_empty_row(row_idx)

        for col_idx in reversed(list_of_empty_cols):
            #self.insert_empty_col(col_idx)
            pass



    def get_galaxy_combinations(self, l):
        list_of_combined_galaxies = []
        list_of_combined_galaxies.extend(combinations(l, 2))
        return list_of_combined_galaxies

    def get_sum_of_galaxy_distances(self):
        sum_of_galaxy_distances = 0
        for pair_of_galaxies in self.list_of_galaxy_combinations:
            distance = abs(pair_of_galaxies[1][0] - pair_of_galaxies[0][0]) + abs(pair_of_galaxies[1][1] - pair_of_galaxies[0][1])
            sum_of_galaxy_distances += distance
        return sum_of_galaxy_distances


class AoC2023_Day11:
    DEBUG = False

    def __init__(self):
        self.commands = self.load_puzzle_input()
        self.universe = Universe(self.commands)
        self.universe.print_matrix()
        self.answer = 0
        self.answer2 = 0

    def load_puzzle_input(self):
        commands = list()
        if AoC2023_Day11.DEBUG:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day11.dbg"
        else:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day11.txt"
        with open(filename) as file:
            for console_output in file:
                commands.append(console_output.rstrip())

        return commands


    def run_AoC(self):
        self.universe.print_matrix()
        self.answer = self.universe.answer


    def run_AoC_part2(self):
        pass

puzzle = AoC2023_Day11()
puzzle.run_AoC()
print(f"done! answer= {puzzle.answer}")
puzzle.run_AoC_part2()
print(f"done! answer2= {puzzle.answer2}")

# 8649704 too low
# 9974721 too high
# 9271959 LUCAS


out, out2 = 0,0

with open("input.txt") as f:
    m = f.readlines()

    rev = list(zip(*m))
    rows = [x for x,c in enumerate(m) if "#" not in c]
    cols = [x for x,c in enumerate(rev) if "#" not in c]

    coords = [(x, y) for y, l in enumerate(m) for x,c in enumerate(l) if c == "#"]
    count = 0
    for i, (x1, y1) in enumerate(coords[:-1]):
        for (x2, y2) in coords[i + 1:]:
            count += 1
            xa = min(x1, x2)
            xe = max(x1, x2)

            ya = min(y1, y2)
            ye = max(y1, y2)

            r = len([y for y in rows if y >= ya and y <= ye])
            cc = len([y for y in cols if y >= xa and y <= xe])

            out += xe - xa + ye - ya + r + cc - r - cc
    print(out)

