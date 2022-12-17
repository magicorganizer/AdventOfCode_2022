
class DayTemplate:
    def __init__(self):
        self.commands = []

    def load_puzzle_input(self):
        self.commands.clear()
        filename = r"/home/holger/PycharmProjects/AdventOfCode/template.txt"
        with open(filename) as file:
            for console_output in file:
                self.commands.append(console_output.rstrip())


puzzle = DayTemplate()
puzzle.load_puzzle_input()
