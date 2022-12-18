from enum import Enum

class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    UNDEFINED = 4

class Track:
    def __init__(self, track_name):
        self.track_name = track_name
        self.pos = [0, 0]
        self.curr_height = chr(ord("a") - 1)
        self.track_status = "searching"  # finished, blocked
        self.next_step = Direction.UNDEFINED
        self.next_step_quality = 100
        self.track = []

    def __str__(self):
        return f"Track {self.track_name} {self.pos} H:{self.curr_height} St:{self.track_status} Dir:{self.next_step} L:{self.track}"

    def step(self):
        self.track.append(self.pos)
        if self.next_step == 0:
            self.pos[0] -= 1
        elif self.next_step == 1:
            self.pos[1] -= 1
        elif self.next_step == 2:
            self.pos[0] += 1
        elif self.next_step == 3:
            self.pos[1] += 1
        print(self.track_name, self.pos)
class Day12:
    def __init__(self):
        self.commands = []
        self.map = []
        self.pos = [0, 0]
        self.map_width = 0
        self.map_height = 0
        self.curr_track_idx = 0
        self.tracks = [Track("init_track")]
        self.track_backlog = []
        self.back_track_idx = 1

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
            self.map[pos[0]][pos[1]] = list_of_chars[list_of_dirs.pop(0)]

    def print_tracks(self):
        print("print tracks")
        for idx, track in enumerate(self.tracks):
            print(idx, track)

    def find_track(self):
        ret_val = False
        for track in self.tracks:
            if track.track_status == "searching":
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
                                print(f"{Direction(idx).name} {delta}")
                                continue_curr_track = False
                            else:
                                # copy track for next possible way
                                new_track = temp_track
                                new_track.next_step_quality = delta
                                new_track.next_step = idx
                                new_track.track_name = f"back_track_{self.back_track_idx}"
                                self.back_track_idx += 1
                                self.track_backlog.append(new_track)
                if number_of_possible_dirs == 0:
                    track.track_status = "blocked"
                self.mark_position_in_matrix(save_track_pos, list_of_dirs)

        for back_track in self.track_backlog:
            self.tracks.append(back_track)
        self.track_backlog.clear()

        for track in self.tracks:
            track.step()
            track.curr_height = self.map[track.pos[0]][track.pos[1]]
            if track.track_status == "searching":
                ret_val = True
        self.print_map()
        return ret_val


puzzle = Day12()
puzzle.load_puzzle_input()
puzzle.fill_map()
puzzle.find_start_point()
while 1:
    puzzle.print_tracks()
    if not puzzle.find_track():

        break
