import logging

logging.basicConfig(level=logging.INFO, filename='AoC2023.log', filemode='w')

class Hand:
    dict_of_cards = {"A":14, "K":13, "Q":12, "J":11, "T":10, "9":9, "8":8, "7":7, "6":6, "5":5, "4":4, "3":3, "2":2}
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.dict_groups = dict()
        self.type = self.get_type_of_hand()
        self.internal_rating = self.calculate_rating()

    def get_type_of_hand(self):
        for card in Hand.dict_of_cards.keys():
            count = self.cards.count(card)
            if count:
                self.dict_groups[card] = count

        type_string = ""
        for card, count in self.dict_groups.items():
            type_string += str(count)
        return sorted(type_string, reverse=True)

    def calculate_rating(self):
        rating = 0

        for item in self.type:
            rating += 10000 ** int(item)

        factor = 1
        for card in reversed(self.cards):
            value = Hand.dict_of_cards[card]
            rating += value * factor
            factor *= 100

        return rating

class AoC2023_Day7:
    DEBUG = False


    def __init__(self):
        self.commands = self.load_puzzle_input()
        self.list_of_hands = list()
        self.answer = 0
        self.answer2 = 0


    def load_puzzle_input(self):
        commands = list()
        if AoC2023_Day7.DEBUG:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day7.dbg"
        else:
            filename = r"/home/holger/PycharmProjects/AdventOfCode/AoC2023_day7.txt"
        with open(filename) as file:
            for console_output in file:
                commands.append(console_output.rstrip())

        return commands

    def run_AoC(self):
        for line in self.commands:
            self.list_of_hands.append(Hand(line.split()[0], int(line.split()[1])))

        # sort list of objects
        self.sorted_list_of_hands = sorted(self.list_of_hands, key=lambda hand: hand.internal_rating)


        rank = 1
        for hand in self.sorted_list_of_hands:
            puzzle.answer += hand.bid * rank
            rank += 1

    def run_AoC_part2(self):
        pass

puzzle = AoC2023_Day7()
puzzle.load_puzzle_input()
puzzle.run_AoC()
print(f"done! answer= {puzzle.answer}")
puzzle.run_AoC_part2()
print(f"done! answer2= {puzzle.answer2}")
#251806503, 251781814