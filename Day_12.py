from enum import Enum

class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    UNDEFINED = 4

class Track:
    def __init__(self):
        self.pos = [0, 0]
        self.curr_height = chr(ord("a") - 1)
        self.track_status = "searching"  # finished, blocked
        self.next_step = Direction.UNDEFINED
        self.next_step_quality = 100
        self.track = []

    def step(self):
        pass

class Day12:
    def __init__(self):
        self.commands = []
        self.map = []
        self.pos = [0, 0]
        self.map_width = 0
        self.map_height = 0
        self.curr_track_idx = 0
        self.tracks = [Track()]
        self.track_backlog = []

    def load_puzzle_input(self):
        self.commands.clear()
        filename = r"/home/holger/PycharmProjects/AdventOfCode/map_for_day_12.txt"
        with open(filename) as file:
            for console_output in file:
                self.commands.append(console_output.rstrip())

    def fill_map(self):
        for line in self.commands:
            list_line = [*line]
            self.map_width = len(list_line)
            self.map.append(list_line)
        self.map_height = len(self.map)

    def find_start_point(self):
        for row_idx, row_list in enumerate(self.map):
            if "S" in row_list:
                index = row_list.index("S")
                if -1 != index:
                    print(f"({row_idx}, {index}")
                    self.pos[0] = index
                    self.pos[1] = row_idx

    def get_best_way(self, pos):
        l = self.map[pos[0]-1][pos[1]] if pos[0] > 0 else "X"
        u = self.map[pos[0]][pos[1]-1] if pos[1] > 0 else "X"
        r = self.map[pos[0]+1][pos[1]] if pos[0] < self.map_width - 1 else "X"
        d = self.map[pos[0]][pos[1]+1] if pos[1] < self.map_height - 1 else "X"
        return [l, u, r, d]

    def print_map(self):
        for row in self.map:
            str_row = ""
            print(str_row.join(row))

    def mark_position_in_matrix(self, pos, list_of_dirs):
        list_of_chars = ["<", "^", ">", "v"]
        if len(list_of_dirs) > 1:
            self.map[pos[0]][pos[1]] = "+"
        else:
            self.map[pos[0]][pos[1]] = list_of_chars[list_of_chars.pop(0)]

    def find_track(self):
        for track in self.tracks:
            save_track_pos = track.pos
            list_of_dirs = []
            list_dir_effort = self.get_best_way(track.pos)
            continue_curr_track = True
            number_of_possible_dirs = 0
            temp_track = track
            for idx, dir in enumerate(list_dir_effort):
                if dir != "X":
                    delta = ord(dir) - ord(track.curr_height)
                    if delta in [1, 0]:
                        list_of_dirs.append(idx)
                        number_of_possible_dirs += 1
                        if continue_curr_track:
                            track.next_step_quality = delta
                            track.next_step = idx
                            track.step()
                            print(f"{Direction(idx).name} {delta}")
                            continue_curr_track = False
                        else:
                            # copy track for next possible way
                            new_track = temp_track
                            new_track.next_step_quality = delta
                            new_track.next_step = idx
                            new_track.step()
                            self.track_backlog.append(new_track)
            if number_of_possible_dirs == 0:
                track.track_status = "blocked"
            self.mark_position_in_matrix(save_track_pos, list_of_dirs)

        self.print_map()


puzzle = Day12()
puzzle.load_puzzle_input()
puzzle.fill_map()
puzzle.find_start_point()
puzzle.find_track()
