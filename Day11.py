DEBUG_LEVEL = "not Full"


class Monkey:
    def __init__(self, monkey_name, initial_list, divisible_by, operation_string, monkey_true, monkey_false, worry_level_divisor):
        self.monkey_name = monkey_name
        self.list_items = [int(str_number) for str_number in initial_list.split(",")]
        self.divisible_by = int(divisible_by)
        self.operation_string = operation_string
        self.monkey_true = int(monkey_true)
        self.monkey_false = int(monkey_false)
        self.inspection_counter = 0
        self.worry_level_divisor = worry_level_divisor
        if DEBUG_LEVEL == "Full":
            print(f"Setup {self.monkey_name}")

    def operation(self, old_level):
        tmp = self.operation_string.split()
        worry_level = old_level
        if tmp[0] == "*":
            worry_level *= old_level if tmp[1] == "old" else int(tmp[1])
        elif tmp[0] == "+":
            worry_level += old_level if tmp[1] == "old" else int(tmp[1])
        else:
            raise Exception("unknown operation")
        return worry_level

    def get_thrown_item(self, item):
        if DEBUG_LEVEL == "Full":
            print(f"throw to {self.monkey_name}")
        self.list_items.append(item)

    def get_thrown_item(self, item):
        if DEBUG_LEVEL == "Full":
            print(f"throw {item} to {self.monkey_name}")
        self.list_items.append(item)

    def print_item_list(self):
        if DEBUG_LEVEL == "Full":
            print(f"{self.monkey_name} {self.list_items} - inspection counter {self.inspection_counter}")

    def run_monkey(self, list_of_monkeys):
        if DEBUG_LEVEL == "Full":
            self.print_item_list()

        while self.list_items:
            item = self.list_items.pop()
            self.inspection_counter += 1
            new_worry_level = self.operation(item)
            decreased_worry_level = int(new_worry_level % self.worry_level_divisor)

            # check divisible by self.divisible_by
            if decreased_worry_level % self.divisible_by == 0:
                list_of_monkeys[self.monkey_true].get_thrown_item(decreased_worry_level)
            else:
                list_of_monkeys[self.monkey_false].get_thrown_item(decreased_worry_level)


class Day11:

    def __init__(self):
        self.commands = []
        self.list_of_monkeys = []
        self.dict_collector = dict()
        self.round_counter = 0
        self.sort_dict = dict()
        self.worry_level_divider = 1
        self.collect_prime_numbers = set()
        self.prime_factor_product = 1

    def load_puzzle_input(self):
        self.commands.clear()

        filename = r"/home/holger/PycharmProjects/AdventOfCode/Monkey in the Middle.txt"

        with open(filename) as file:
            for console_output in file:
                self.commands.append(console_output.rstrip())

    def setup_monkeys(self):
        self.round_counter = 0
        self.list_of_monkeys.clear()

        for command in self.commands:
            if ":" in command:
                tmp = command.split(":")
                if len(tmp) > 1:
                    if tmp[1]:
                        key = tmp[0].lstrip()
                        value = tmp[1].lstrip()
                    else:
                        key = "Name"
                        value = tmp[0]
                self.dict_collector[key] = value
            if "If false" in self.dict_collector.keys():
                # setup class initial_list, divisible_by, operation_string
                monkey = Monkey(
                    self.dict_collector["Name"],
                    self.dict_collector["Starting items"],
                    self.dict_collector["Test"].replace("divisible by ", ""),
                    self.dict_collector["Operation"].replace("new = old ", ""),
                    self.dict_collector["If true"].replace("throw to monkey ", ""),
                    self.dict_collector["If false"].replace("throw to monkey ", ""),
                    self.prime_factor_product
                )
                self.list_of_monkeys.append(monkey)
                self.dict_collector.clear()

    def calculate_lcd(self):
        for monkey in self.list_of_monkeys:
            for item in monkey.list_items:
                self.collect_prime_numbers.add(item)
        for prime_number in self.collect_prime_numbers:
            self.prime_factor_product *= prime_number
        print(self.prime_factor_product)

    def monkeys_play_keep_away(self, prime_factor_product):
        for self.round_counter in range(1, 10001):
            for monkey in self.list_of_monkeys:
                monkey.worry_level_divisor = prime_factor_product
                monkey.run_monkey(self.list_of_monkeys)
            # ret_val, match_to_round = self.check_results_after_several_rounds()
            # if match_to_round:
            #     if not ret_val:
            #         #print(f"ERROR: Missmatch at round {self.round_counter}")
            #         return False
            #     else:
            #         print(f"Match at {self.worry_level_divider} at round {self.round_counter}")
        # ret_val, match_to_round = self.check_results_after_several_rounds()
        # if ret_val:
        #     print("final match")
        for monkey in self.list_of_monkeys:
            self.sort_dict[monkey.inspection_counter] = monkey.list_items
            monkey.print_item_list()
        self.calc_monkey_business_level()

    def calc_monkey_business_level(self):
        sort_data = sorted(self.sort_dict.items(), reverse=True)
        sort_data_dict = dict(sort_data)
        monkey_business_level = 1
        for idx, monkey_list in enumerate(sort_data_dict.items()):
            if idx < 2:
                monkey_business_level *= monkey_list[0]
        print(monkey_business_level)

    def check_results_after_several_rounds(self):
        dict_rounds_to_check = {
            1: [2, 4, 3, 6],
            20: [99, 97, 8, 103],
            1000: [5204, 4792, 199, 5192],
            2000: [10419, 9577, 392, 10391],
            3000: [15638, 14358, 587, 15593],
            4000: [20858, 19138, 780, 20797],
            5000: [26075, 23921, 974, 26000],
            6000: [31294, 28702, 1165, 31204],
            7000: [36508, 33488, 1360, 36400],
            8000: [41728, 38268, 1553, 41606],
            9000: [46945, 43051, 1746, 46807],
            10000: [52166, 47830, 1938, 52013]
        }
        ret_val = True
        if self.round_counter in dict_rounds_to_check.keys():
            match_to_round = True
            for idx, monkey in enumerate(self.list_of_monkeys):
                if not monkey.inspection_counter == dict_rounds_to_check[self.round_counter][idx]:
                    ret_val = False
                    # print(f"{self.round_counter} {idx} - {monkey.inspection_counter} expected {dict_rounds_to_check[self.round_counter][idx]}")
        else:
            match_to_round = False
        return ret_val, match_to_round


puzzle = Day11()
puzzle.load_puzzle_input()
puzzle.setup_monkeys()
puzzle.calculate_lcd()
puzzle.monkeys_play_keep_away(puzzle.prime_factor_product)
