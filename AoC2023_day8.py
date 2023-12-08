import logging

logging.basicConfig(level=logging.INFO, filename='AoC2023.log', filemode='w')

class Map:
    def __init__(self, lr_instructions):
        self.lr_instructions = [*lr_instructions]
        self.dict_decision = dict()
        self.steps = 0

    def add_decision_item(self, node, tupel_lr):
        self.dict_decision[node] = tupel_lr

    def get_next_node(self, node_name, direction):
        self.steps += 1
        next_node_name = self.dict_decision[node_name][direction]
        return next_node_name.lstrip()

    def get_next_direction(self):
        dir_char = self.lr_instructions.pop(0)
        self.lr_instructions.append(dir_char)
        return 0 if dir_char == "L" else 1

    def map_run(self):
        node_name = "AAA"
        while 1:
            node_name = self.get_next_node(node_name,self.get_next_direction())
            if node_name == "ZZZ":
                break

        return self.steps


class AoC2023_Day8:
    DEBUG = False

    def __init__(self):
        self.commands = self.load_puzzle_input()
        self.list_of_hands = list()
        self.map = None
        self.answer = 0
        self.answer2 = 0


    def load_puzzle_input(self):
        commands = list()
        if AoC2023_Day8.DEBUG:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day8.dbg"
        else:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day8.txt"
        with open(filename) as file:
            for console_output in file:
                commands.append(console_output.rstrip())

        return commands

    def run_AoC(self):
        for idx, line in enumerate(self.commands):
            if idx == 0:
                self.map = Map(line)
            else:
                if line:
                    splitted_line = line.split(" = ")
                    tmp = splitted_line[1][1:-1].split(",")
                    self.map.add_decision_item(splitted_line[0],(tmp[0],tmp[1]))
        self.answer = self.map.map_run()

    def run_AoC_part2(self):
        pass

puzzle = AoC2023_Day8()
puzzle.run_AoC()
print(f"done! answer= {puzzle.answer}")
puzzle.run_AoC_part2()
print(f"done! answer2= {puzzle.answer2}")
#251806503, 251781814