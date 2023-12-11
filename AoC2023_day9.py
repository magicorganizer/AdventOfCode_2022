import logging

logging.basicConfig(level=logging.INFO, filename='AoC2023.log', filemode='w')

class Sequence:
    def __init__(self, sequence_string):
        self.sequence = [int(item) for item in sequence_string.split()]
        self.prediction = 0
        self.list_of_temp_sequences = list()
        self.list_of_temp_sequences.append(self.sequence)
        self.do_prediction()

    def __str__(self):
        return f"{self.sequence} ... {self.prediction}  len({len(self.list_of_temp_sequences)})"

    def do_prediction(self):
        while 1:
            last_list = self.list_of_temp_sequences[-1]
            # calculate difference between elements... len new list is len old list - 1
            difference_list = [j-i for i, j in zip(last_list[:-1], last_list[1:])]
            self.list_of_temp_sequences.append(difference_list)
            if sum(difference_list) == 0:
                break

        # calculate prediction by backwards adding all last list elements
        last_elements = list()
        for templist in reversed(self.list_of_temp_sequences):
            last_elements.append(templist[-1])

        self.prediction = sum(last_elements)




class AoC2023_Day9:
    DEBUG = False

    def __init__(self):
        self.commands = self.load_puzzle_input()
        self.list_of_sequences = list()
        self.answer = 0
        self.answer2 = 0

    def load_puzzle_input(self):
        commands = list()
        if AoC2023_Day9.DEBUG:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day9.dbg"
        else:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day9.txt"
        with open(filename) as file:
            for console_output in file:
                commands.append(console_output.rstrip())

        return commands

    def run_AoC(self):
        for line in self.commands:
            self.list_of_sequences.append(Sequence(line))

        for sequence in self.list_of_sequences:
            self.answer += sequence.prediction
            print(sequence)

    def run_AoC_part2(self):
        pass

puzzle = AoC2023_Day9()
puzzle.run_AoC()
print(f"done! answer= {puzzle.answer}")
puzzle.run_AoC_part2()
print(f"done! answer2= {puzzle.answer2}")
#1789635121 too low