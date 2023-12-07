import logging

logging.basicConfig(level=logging.INFO, filename='AoC2023.log', filemode='w')


class AoC2023_Day1:
    DEBUG = False

    def __init__(self):
        self.commands = []
        self.answer = 0

    def load_puzzle_input(self):
        self.commands.clear()
        if AoC2023_Day1.DEBUG:
            filename = r"d:\Data\Advent Of Code 2023\AoC2023_Day1.dbg"
        else:
            filename = r"d:\Data\Advent Of Code 2023\AoC2023_Day1.txt"
        with open(filename) as file:
            for console_output in file:
                self.commands.append(console_output.rstrip())

    def run_AoC(self):
        for line in self.commands:
            raw_line = line
            logging.info(f"{raw_line}")

    def run_AoC_second_implementation(self):
        pass


puzzle = AoC2023_Day1()
puzzle.load_puzzle_input()
puzzle.run_AoC()
print(f"done! answer= {puzzle.answer}")
