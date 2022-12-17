import re
"""
[Q] [J]                         [H]
[G] [S] [Q]     [Z]             [P]
[P] [F] [M]     [F]     [F]     [S]
[R] [R] [P] [F] [V]     [D]     [L]
[L] [W] [W] [D] [W] [S] [V]     [G]
[C] [H] [H] [T] [D] [L] [M] [B] [B]
[T] [Q] [B] [S] [L] [C] [B] [J] [N]
[F] [N] [F] [V] [Q] [Z] [Z] [T] [Q]
 1   2   3   4   5   6   7   8   9
"""
all_stacks = [
    [],                                        # temp stack
    ["F", "T", "C", "L", "R", "P", "G", "Q"],  # stack 1
    ["N", "Q", "H", "W", "R", "F", "S", "J"],  # stack 2
    ["F", "B", "H", "W", "P", "M", "Q"],       # stack 3
    ["V", "S", "T", "D", "F"],                 # stack 4
    ["Q", "L", "D", "W", "V", "F", "Z"],       # stack 5
    ["Z", "C", "L", "S"],                      # stack 6
    ["Z", "B", "M", "V", "D", "F"],            # stack 7
    ["T", "J", "B"],                           # stack 8
    ["Q", "N", "B", "G", "L", "S", "P", "H"]   # stack 9
]


def print_stacks():
    for stack in all_stacks:
        print(stack)


def print_top_crates():
    result = ""
    for idx, stack in enumerate(all_stacks):
        if idx > 0:
            result += stack.pop()
    print(result)


def apply_cran_command(command, sub_command="" ):
    match_object = re.match("move (.*) from (.*) to (.*)", command)
    if match_object:
        origin = int(match_object.group(2))
        destination = int(match_object.group(3))
        count = int(match_object.group(1))

        if sub_command == "multiple":
            for i in range(count):
                all_stacks[0].append(all_stacks[origin].pop())

            #print("stack to dest")
            for i in range(count):
                all_stacks[destination].append(all_stacks[0].pop())
        else:
            for i in range(count):
                all_stacks[destination].append(all_stacks[origin].pop())

        #print_stacks()
    else:
        raise "I didn't get the command"

filename = r"/home/holger/PycharmProjects/AdventOfCode/crane_commands.txt"
with open(filename) as file:
    for command in file:
        apply_cran_command(command.rstrip(), "multiple")

#print_stacks()
print_top_crates()
