class AoC2023_Day1:
    def __init__(self):
        self.commands = []
        self.sum = 0

    def load_puzzle_input(self):
        self.commands.clear()
        filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_Day1.txt"
        with open(filename) as file:
            for console_output in file:
                self.commands.append(console_output.rstrip())

    def run_AoC(self):
        for line in self.commands:
            line = self.consider_diget_strings(line)
            list_of_chars = [*line]
            list_of_numbers = []
            for character in list_of_chars:
                if character.isnumeric():
                    list_of_numbers.append(character)
            if list_of_numbers:
                number = list_of_numbers[0]
                number += list_of_numbers[-1]
                self.sum += int(number)

    def consider_diget_strings(self, out_string):
        dict_lookup_table = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}

        #find first digit string
        for idx in range(len(out_string)+1):
            tempstring = out_string[:idx]
            for key, value in sorted(dict_lookup_table.items(), reverse=True):
                if key in tempstring:
                    out_string = out_string.replace(key, str(value))
        print(out_string)
        return out_string


puzzle = AoC2023_Day1()
puzzle.load_puzzle_input()
puzzle.run_AoC()
print(f"done! answer= {puzzle.sum}")
