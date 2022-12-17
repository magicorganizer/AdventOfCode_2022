import re
import os

list_test_commands = [
"$ cd /",
"$ ls",
"dir a",
"14848514 b.txt",
"8504156 c.dat",
"dir d",
"$ cd a",
"$ ls",
"dir e",
"29116 f",
"2557 g",
"62596 h.lst",
"$ cd e",
"$ ls",
"584 i",
"$ cd ..",
"$ cd ..",
"$ cd d",
"$ ls",
"4060174 j",
"8033020 d.log",
"5626152 d.ext",
"7214296 k",
]

current_path = ""

dict_dataisystem = {}
dict_dir_sizes = {}


def handle_command(console_output, current_path):
    regex_string = r'\$ cd (.*)'
    matchObj = re.match(regex_string, console_output, re.M | re.I)
    if matchObj:
        dir = matchObj.group(1)
        if dir == "/":
            current_path = "root"
        elif dir == "..":
            current_path = current_path[:current_path.rfind('/')]
        else:
            current_path += f"/{dir}"
    else:
        print(f"unhandled command {console_output}")
    return current_path

def handle_data(console_output, current_path, dict_dataisystem, dict_dir_sizes):
    regex_string = r'(.*) (.*)'
    matchObj = re.match(regex_string, console_output, re.M | re.I)
    if matchObj:
        param1 = matchObj.group(1)
        param2 = matchObj.group(2)

        if param1 == "dir":
            print(f"{current_path} {param2} (dir)")
        else:
            dict_dataisystem[f"{current_path}/{param2}"] = (param2, param1)
            print(f"{current_path} {param2} (file, {param1})")

            # add file size to all dirs of path
            list_of_dirs = current_path.split("/")
            for dir in list_of_dirs:
                size = dict_dir_sizes.get(dir, 0)
                size += int(param1)
                dict_dir_sizes[dir] = size


filename = r"/home/holger/PycharmProjects/AdventOfCode/console_output.txt"
with open(filename) as file:
    #for console_output in list_test_commands:
    for console_output in file:
        console_output = console_output.rstrip()
        if "$" == console_output[0]:
            current_path = handle_command(console_output, current_path)
        else:
            handle_data(console_output, current_path, dict_dataisystem, dict_dir_sizes)

sum = 0
for key, value in dict_dir_sizes.items():
    print(key, value)
    if value < 100000:
        sum += value

print(sum)
