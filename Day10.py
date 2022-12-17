import re

dict_inst_cycles = {
    "noop": 1,
    "addx": 2
}

class Day10:
    def __init__(self):
        self.commands = []
        self.register_x = 1
        self.cycle_counter = 0
        self.cpu_state = "idle"
        self.current_command = ""
        self.instruction = ""
        self.value = None
        self.cycles_remaining = -1
        self.signal_strength = 0
        self.sum_signal_strength = 0
        self.display_row = 0
        self.display = []
        self.display_row_string = ""

    def load_puzzle_input(self):
        self.commands.clear()
        filename = r"/home/holger/PycharmProjects/AdventOfCode/elves_assembler_instructions_tiny.txt"
        with open(filename) as file:
            for console_output in file:
                self.commands.append(console_output.rstrip())

    def get_next_command(self):
        command = None
        if self.commands:
            command = self.commands.pop(0)
        return command

    def process_command(self):
        self.cycles_remaining -= 1
        if not self.cycles_remaining:
            if self.value:
                self.register_x += self.value
            self.cpu_state = "idle"

    def display_driver(self):
        cycle_counter = self.cycle_counter - 1
        picel_x = cycle_counter % 40

        sprite = []
        sprite.append(self.register_x - 1)
        sprite.append(self.register_x)
        sprite.append(self.register_x + 1)
        self.display_row_string += "#" if picel_x in sprite else "."
        if picel_x == 39:
            self.display.append(self.display_row_string)
            self.display_row_string = ""


    def run_elves_cpu(self):
        while 1:
            self.cycle_counter += 1
            if self.cpu_state == "idle":
                self.current_command = self.get_next_command()
                if not self.current_command:
                    return

                print(self.current_command)

                self.cpu_state = f"running {self.current_command}"
                self.analyse_current_command()
            self.get_snapshot()
            self.display_driver()
            self.process_command()
            print(f"cyclecnt {self.cycle_counter} reg x {self.register_x}")
            #self.get_snapshot()

    def get_snapshot(self):
        if self.cycle_counter in [20, 60, 100, 140, 180,220]:
            self.signal_strength = self.cycle_counter * self.register_x
            self.sum_signal_strength += self.signal_strength
            snapshot = f"Signalstrength {self.signal_strength} at {self.cycle_counter}"
            print(snapshot)

    def analyse_current_command(self):
        splitted_command = self.current_command.split()
        self.instruction = splitted_command[0]
        self.cycles_remaining = dict_inst_cycles[self.instruction]
        if len(splitted_command) > 1:
            self.value = int(self.current_command.split()[1])
        else:
            self.value = None


puzzle = Day10()
puzzle.load_puzzle_input()
puzzle.run_elves_cpu()
print(f"Sum cycle srength {puzzle.sum_signal_strength}")

for row_string in puzzle.display:
    print(row_string)

# ZGCJZJFL