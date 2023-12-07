import logging
import re

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
        for matrix_row in self.matrix:
            print(matrix_row)

    def get_element_xy(self, x, y):
        if x in range(0, self.max_x) and y in range(0, self.max_y):
            return self.matrix[y][x]
        else:
            return None

    def set_element_xy(self, x, y, char):
        self.matrix[y][x] = char


class PartNumber:
    def __init__(self, number, start_coordinate, row, matrix):
        self.number = int(number)
        if self.number == 515 and row == 138:
            print("trap")
        self.matrix = matrix
        self.list_coordiates = [(idx, row) for idx in range(start_coordinate, start_coordinate + len(number))]
        self.list_neighbors = self.get_neighbors_of_number()
        self.is_partnumber = self.is_symbol_in_list_of_neighbors()
        # if self.is_partnumber:
        #     for coord in self.list_coordiates:
        #         self.matrix.set_element_xy(coord[0], coord[1], "X")

    def get_neighbors(self, tupel_xy):
        list_neighbors_of_tupel = list()
        x = tupel_xy[0]
        y = tupel_xy[1]
        for xn in range(x - 1, x + 2):
            for yn in range(y - 1, y + 2):
                list_neighbors_of_tupel.append((xn, yn, self.matrix.get_element_xy(xn, yn)))
        return list_neighbors_of_tupel

    def get_neighbors_of_number(self):
        list_of_neighbors = list()
        for coordinate_number in self.list_coordiates:
            list_of_neighbors.extend(self.get_neighbors(coordinate_number))
        list_of_neighbors = list(set(list_of_neighbors) - set(self.list_coordiates))
        return list_of_neighbors

    @staticmethod
    def is_symbol(character):
        if character in ['#', '$', '%', '&', '*', '+', '-', '/', '=', '@']:
            return True
        else:
            return False

    def is_symbol_in_list_of_neighbors(self):
        is_partnumber = False
        for neighbor in self.list_neighbors:
            character = self.matrix.get_element_xy(neighbor[0], neighbor[1])
            if character:
                if self.is_symbol(character):
                    is_partnumber = True

        return is_partnumber


class AoC2023_Day3:
    DEBUG = False

    def __init__(self):
        self.commands = self.load_puzzle_input()
        self.matrix_of_symbols = Matrix(self.commands)
        self.list_of_numbers = list()
        self.answer = 0
        self.answer2 = 0
        self.dict_of_gearindicators = dict()

    def load_puzzle_input(self):
        commands = list()
        if AoC2023_Day3.DEBUG:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day3.dbg"
        else:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day3.txt"
        with open(filename) as file:
            for console_output in file:
                commands.append(console_output.rstrip())

        return commands

    def get_numbers_per_line(self, string, row):
        list_of_partnumbers_per_line = list()
        #numbers = [num for num in re.findall(r'\d+', string)]
        numbers = list()
        p = re.compile("\d+")
        for m in p.finditer(string):
            number = m.group()
            idx = m.start()
            numbers.append((number, idx))

        for number_tupel in numbers:
            number = number_tupel[0]
            idx = int(number_tupel[1])
            list_of_partnumbers_per_line.append(PartNumber(number, idx, row, self.matrix_of_symbols))

        return list_of_partnumbers_per_line


    def run_AoC(self):
        for row, line in enumerate(self.commands):
            self.list_of_numbers.extend(self.get_numbers_per_line(line, row))

        for number in self.list_of_numbers:
            if number.is_partnumber:
                self.answer += number.number
            print(f"partnumber: {number.number} is Partnumber {number.is_partnumber}")

        self.matrix_of_symbols.print_matrix()


    def run_AoC_part2(self):
        for part_number in self.list_of_numbers:
            if part_number.is_partnumber:
                # get "*" and its pos and number if it has two partners it's a gear ratio
                for symbol in part_number.list_neighbors:
                    symbol_x = symbol[0]
                    symbol_y = symbol[1]
                    symbol_char = symbol[2]
                    if symbol_char == "*":
                        key = f"*-{symbol_x}-{symbol_y}"
                        tmp_list = self.dict_of_gearindicators.get(key, [])
                        tmp_list.append(part_number)
                        self.dict_of_gearindicators[key] = tmp_list

        # check for gear symbols on two partners
        for key, gear_symbol_list in self.dict_of_gearindicators.items():
            count = len(gear_symbol_list)
            if count > 1:
                if count != 2:
                    print("Error")
                gear_ratio = gear_symbol_list[0].number * gear_symbol_list[1].number
                self.answer2 += gear_ratio


puzzle = AoC2023_Day3()
puzzle.run_AoC()
puzzle.run_AoC_part2()

print(f"done! answer= {puzzle.answer}")
if puzzle.answer in [528552, 82964, 83329]:
    print(f"Ist aber falsch!")
if puzzle.answer == 527369:
    print("und richtig")
print(f"done! answer2= {puzzle.answer2}")