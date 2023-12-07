import logging

logging.basicConfig(level=logging.INFO, filename='AoC2023.log', filemode='w')

class Race:
    def __init__(self, race_time, distance):
        self.race_time = race_time
        self.distance = distance
        self.list_of_options_to_win = self.calculate_options_to_win()

    def calculate_options_to_win(self):
        list_of_options = list()
        for button_time in range(self.race_time + 1):
            run_time = self.race_time - button_time
            speed = button_time
            dist = speed * run_time
            if dist > self.distance:
                list_of_options.append(button_time)
        return list_of_options


class AoC2023_Day6:
    DEBUG = False

    def __init__(self):
        self.commands = self.load_puzzle_input()
        self.list_of_races = list()
        self.answer = 1
        self.answer2 = 1


    def load_puzzle_input(self):
        commands = list()
        if AoC2023_Day6.DEBUG:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day6.dbg"
        else:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day6.txt"
        with open(filename) as file:
            for console_output in file:
                commands.append(console_output.rstrip())

        return commands

    def run_AoC(self):
        list_time = [int(time) for time in self.commands[0].split(":")[1].lstrip().split()]
        list_dist = [int(dist) for dist in self.commands[1].split(":")[1].lstrip().split()]
        races = zip(list_time, list_dist)

        for race_data in races:
            self.list_of_races.append(Race(race_data[0], race_data[1]))


        for race in self.list_of_races:
            self.answer *= len(race.list_of_options_to_win)
            #logging.info(f"{line}")

    def run_AoC_part2(self):
        self.list_of_races.clear()
        list_time = [int(self.commands[0].split(":")[1].replace(" ", ""))]
        list_dist = [int(self.commands[1].split(":")[1].replace(" ", ""))]
        races = zip(list_time, list_dist)

        for race_data in races:
            self.list_of_races.append(Race(race_data[0], race_data[1]))

        for race in self.list_of_races:
            self.answer2 *= len(race.list_of_options_to_win)



puzzle = AoC2023_Day6()
puzzle.load_puzzle_input()
puzzle.run_AoC()
print(f"done! answer= {puzzle.answer}")
puzzle.run_AoC_part2()
print(f"done! answer2= {puzzle.answer2}")
