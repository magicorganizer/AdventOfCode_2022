
class Day9:
    def __init__(self):
        #self.SCREEN_SIZE = 20
        #self.OFFSET = int(self.SCREEN_SIZE / 2)
        self.SCREEN_SIZE = 6
        self.OFFSET = 0
        self.screen = []
        self.pos_head = [0, 0]
        self.pos_tail = [0, 0]
        self.pos_list = [[0, 0],
                         [0, 0],
                         [0, 0],
                         [0, 0],
                         [0, 0],
                         [0, 0],
                         [0, 0],
                         [0, 0],
                         [0, 0],
                         [0, 0]]
        self.set_tail_positions = list()
        self.commands = ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]

    def load_puzzle_input(self):
        self.commands.clear()
        filename = r"/home/holger/PycharmProjects/AdventOfCode/rope_commands.txt"
        with open(filename) as file:
            for console_output in file:
                self.commands.append(console_output.rstrip())

    def print_rope(self, text=""):
        self.screen = []
        for y in range(self.SCREEN_SIZE):
            str_line = "." * self.SCREEN_SIZE
            line = [*str_line]
            self.screen.append(line)

        self.screen[self.OFFSET][self.OFFSET] = "S"
        for idx in range(9, -1, -1):
            x = self.pos_list[idx][0]
            y = self.pos_list[idx][1]
            try:
                self.screen[y + self.OFFSET][x + self.OFFSET] = str(idx)
            except IndexError:
                pass

        print(text)
        for line in reversed(self.screen):
            str_line = ""
            print(str_line.join(line))

    def simulate_tail(self, command):
        for idx in range(1, 10):
            last_idx = idx - 1
            diff_x = self.pos_list[last_idx][0] - self.pos_list[idx][0]
            diff_y = self.pos_list[last_idx][1] - self.pos_list[idx][1]
            print(f"Diffs {diff_x}, {diff_y}")
            if abs(diff_x) < 2 and abs(diff_y) < 2:
                pass
            else:
                if abs(diff_x) > abs(diff_y):
                    # L or R
                    if diff_x > 0:
                        # R
                        if abs(diff_y) < 2:
                            self.pos_list[idx][0] += 1
                            self.pos_list[idx][1] = self.pos_list[last_idx][1]
                        else:
                            self.pos_list[idx][0] += 1
                            self.pos_list[idx][1] = int(diff_y / 2)
                    else:
                        # L
                        if abs(diff_y) < 2:
                            self.pos_list[idx][0] -= 1
                            self.pos_list[idx][1] = self.pos_list[last_idx][1]
                        else:
                            self.pos_list[idx][0] -= 1
                            self.pos_list[idx][1] = int(diff_y / 2)
                else:
                    # U or D
                    if diff_y > 0:
                        # U
                        if abs(diff_x) < 2:
                            self.pos_list[idx][1] += 1
                            self.pos_list[idx][0] = self.pos_list[last_idx][0]
                        else:
                            self.pos_list[idx][1] += 1
                            self.pos_list[idx][0] += int(diff_x / 2)
                    else:
                        # D
                        if abs(diff_x) < 2:
                            self.pos_list[idx][1] -= 1
                            self.pos_list[idx][0] = self.pos_list[last_idx][0]
                        else:
                            self.pos_list[idx][1] -= 1
                            self.pos_list[idx][0] += int(diff_x / 2)
        self.set_tail_positions.append(f"{self.pos_list[9][0]} {self.pos_list[9][1]}")


    def step(self, command):
        direction = command[0]
        step_width = int(command[1])

        for single_step in range(step_width):
            if "U" == direction:
                self.pos_head[1] += 1
                self.pos_list[0][1] += 1
            if "D" == direction:
                self.pos_head[1] -= 1
                self.pos_list[0][1] -= 1
            if "L" == direction:
                self.pos_head[0] -= 1
                self.pos_list[0][0] -= 1
            if "R" == direction:
                self.pos_head[0] += 1
                self.pos_list[0][0] += 1
            self.simulate_tail(command)
            self.print_rope(f"{command}:{single_step}")

    def run_simulation(self):
        for command in self.commands:
            command = command.rsplit()
            print(command)
            self.step(command)

puzzle = Day9()
puzzle.load_puzzle_input()
puzzle.run_simulation()

print(len(puzzle.set_tail_positions))
puzzle.set_tail_positions = list(dict.fromkeys(puzzle.set_tail_positions))
print(len(puzzle.set_tail_positions))