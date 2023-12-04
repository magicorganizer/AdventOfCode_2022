import logging


logging.basicConfig(level=logging.INFO, filename='AoC2023.log', filemode='w')

class CubeGame:

    def __init__(self, game_raw_data):
        self.dict_max_cubes = {
            "red": 12,
            "green": 13,
            "blue": 14
        }
        self.game_raw_data = game_raw_data
        self.game_id = None
        self.list_of_games = None
        self.game_possible = self.auto_run()
        self.power_of_colors = self.part2()

    def auto_run(self):
        # get game id
        self.game_id = self.game_raw_data.split(":")[0]
        self.game_id = self.game_id.replace("Game ", "")
        self.list_of_games = self.game_raw_data.split(":")[1].split(";")

        # check if game is possible
        for game in self.list_of_games:
            if game:
                raw_cubes = game.split(",")
                for cube in raw_cubes:
                    cube = cube.lstrip(" ")
                    parts = cube.split(" ")
                    count = parts[0]
                    color = parts[1]
                    try:
                        if int(count) > self.dict_max_cubes[color]:
                            return False
                    except:
                        pass

        return True

    def part2(self):
        power_of_colors = 0
        # get game id
        self.game_id = self.game_raw_data.split(":")[0]
        self.game_id = self.game_id.replace("Game ", "")
        self.list_of_games = self.game_raw_data.split(":")[1].split(";")
        dict_collect_colors = {
            "red": [],
            "green": [],
            "blue": []
        }
        # check if game is possible
        for game in self.list_of_games:
            if game:
                raw_cubes = game.split(",")
                for cube in raw_cubes:
                    cube = cube.lstrip(" ")
                    parts = cube.split(" ")
                    count = parts[0]
                    color = parts[1]
                    dict_collect_colors[color].append(int(count))
        # get max of each color
        max_red = max(dict_collect_colors["red"])
        max_blue = max(dict_collect_colors["blue"])
        max_green = max(dict_collect_colors["green"])
        power_of_colors = max_red * max_blue * max_green

        return power_of_colors



class AoC2023_Day2:
    DEBUG = False

    def __init__(self):
        self.commands = []
        self.answer = 0

    def load_puzzle_input(self):
        self.commands.clear()
        if AoC2023_Day2.DEBUG:
            filename = r"/AoC2023_day3.dbg"
        else:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day2.txt"
        with open(filename) as file:
            for console_output in file:
                self.commands.append(console_output.rstrip())

    def run_AoC(self):
        for line in self.commands:
            raw_line = line

            game_n = CubeGame(raw_line)
            #part1
            # if game_n.game_possible:
            #     self.answer += int(game_n.game_id)

            #part2
            self.answer += game_n.power_of_colors

            logging.info(f"{raw_line}")

    def run_AoC_second_implementation(self):
        pass


puzzle = AoC2023_Day2()
puzzle.load_puzzle_input()
puzzle.run_AoC()
print(f"done! answer= {puzzle.answer}")
