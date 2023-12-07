from enum import Enum

class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    UNDEFINED = 4

class Track:
    def __init__(self, track_name, height=chr(ord("z")+1), pos=[0, 0], track=[]):
        self.track_name = track_name
        self.pos = pos
        self.curr_height = height
        self.track_status = "searching"
        self.next_step = Direction.UNDEFINED
        self.track = track

    def __str__(self):
        return f"Track {self.track_name} size:{len(self.track)} {self.pos} H:{self.curr_height} St:{self.track_status} Dir:{self.next_step} L:{self.track}"

    def step(self):
        if self.next_step == 0:
            self.pos[1] -= 1
        elif self.next_step == 1:
            self.pos[0] -= 1
        elif self.next_step == 2:
            self.pos[1] += 1
        elif self.next_step == 3:
            self.pos[0] += 1
        pos = [self.pos[1], self.pos[0]]
        self.track.append(pos)
        try:
            self.curr_height = puzzle.map[self.pos[0]][self.pos[1]]
        except IndexError:
            self.track_status = "blocked"

class Day12:
    def __init__(self):
        self.commands = []
        self.map = []
        self.map_inverted = []
        self.pos = [0, 0]
        self.map_width = 0
        self.map_height = 0
        self.curr_track_idx = 0
        self.tracks = []
        self.track_backlog = []
        self.back_track_idx = 1
        self.all_used_positions = []
        self.all_explored_positions = []
        self.round_counter = 0
        self.doble_count = 0
        self.blocked_count = 0
        self.exception_counter = 0
        self.shortest_finished_track = ["no list name", 1000000000000]

    def load_puzzle_input(self):
        self.commands.clear()
        filename = r"d:\Data\Advent Of Code 2022\GitHub\AdventOfCode_2022\map_for_day_12_small.txt"
        with open(filename) as file:
            for console_output in file:
                self.commands.append(console_output.rstrip())

    def fill_map(self):
        for line in self.commands:
            list_line = [*line]
            self.map_width = len(list_line)
            black_line = [*" " * self.map_width]
            self.map_inverted.append(black_line)
            self.map.append(list_line)
        self.map_height = len(self.map)

    def find_start_point(self):
        for row_idx, row_list in enumerate(self.map):
            if "E" in row_list:
                index = row_list.index("E")
                if -1 != index:
                    print(f"({row_idx}, {index}")
                    self.pos[0] = row_idx
                    self.pos[1] = index
        self.tracks.append(Track("init_track", pos=[self.pos[0], self.pos[1]], track=[[self.pos[1], self.pos[0]]]))

    def is_new_explored_position(self, y, x):
        exploring_pos = [x, y]
        if exploring_pos not in self.all_explored_positions:
            self.all_explored_positions.append(exploring_pos)
            return True
        else:
            return True

    def get_best_way(self, pos, track):
        if pos not in puzzle.all_used_positions:
            puzzle.all_used_positions.append(pos)
        else:
            track.track_status = "doble"
            self.doble_count += 1
            return ["X", "X", "X", "X"]

        l = (self.map[pos[0]][pos[1]-1] if pos[1] > 0 else "X") if self.is_new_explored_position(pos[0], pos[1]-1) else "D"
        u = (self.map[pos[0]-1][pos[1]] if pos[0] > 0 else "X") if self.is_new_explored_position(pos[0]-1, pos[1]) else "D"
        r = (self.map[pos[0]][pos[1]+1] if pos[1] < self.map_width - 1 else "X") if self.is_new_explored_position(pos[0], pos[1]+1) else "D"
        d = (self.map[pos[0]+1][pos[1]] if pos[0] < self.map_height - 1 else "X") if self.is_new_explored_position(pos[0]+1, pos[1]) else "D"
        return [l, u, r, d]

    def get_list_of_deltas(self, track_curr_height, list_dir_effort):
        list_of_deltas = []
        for item in list_dir_effort:
            list_of_deltas.append(ord(item) - ord(track_curr_height))
        if -1 in list_of_deltas:
            return [-1, 0]
        # if 0 in list_of_deltas:
        #     return [0, -1, -2]
        deltas = list(range(-1, 30))
        return deltas

    def print_map(self, print_inverted=False):
        if print_inverted:
            map = self.map_inverted
        else:
            map = self.map

        for row in map:
            str_row = ""
            print(str_row.join(row))

    def print_finished_track(self):
        for track in self.tracks:
            if track.track_status == "finished":
                for pos in track.track:
                    try:
                        self.map_inverted[pos[1]][pos[0]] = self.map[pos[1]][pos[0]]
                        self.map[pos[1]][pos[0]] = " "
                    except IndexError:
                        self.exception_counter += 1
                break
        self.print_map(print_inverted=False)
        print("*******************************************************************************")
        self.print_map(print_inverted=True)

    def mark_position_in_matrix(self, pos, list_of_dirs):
        list_of_chars = ["<", "^", ">", "v"]
        if len(list_of_dirs) > 1:
            self.map[pos[0]][pos[1]] = "+"
        else:
            self.map[pos[0]][pos[1]] = list_of_chars[list_of_dirs.pop(0)]

    def print_tracks(self, max_list_size=25):
        print(f"{self.round_counter} print tracks {len(self.tracks)}")
        if len(self.tracks) < max_list_size:
            for idx, track in enumerate(self.tracks):
                if track.track_status == "finished" and len(track.track) < self.shortest_finished_track[1]:
                    self.shortest_finished_track[1] = len(track.track)
                    self.shortest_finished_track[0] = track.track_name
                print(idx, track)
            print(f"After round:{self.round_counter} shortest Track: {self.shortest_finished_track}")

    def find_track(self):
        ret_val = True
        self.round_counter += 1
        for track in self.tracks:
            if track.track_status == "searching":
                list_of_dirs = []
                list_dir_effort = self.get_best_way(track.pos, track)
                if track.track_status == "doble":
                    continue
                list_accepted_deltas = self.get_list_of_deltas(track.curr_height, list_dir_effort)
                number_of_possible_dirs = 0
                for idx, dir in enumerate(list_dir_effort):
                    if dir not in ["X", "D"]:
                        delta = ord(dir) - ord(track.curr_height)
                        if delta in list_accepted_deltas:
                            list_of_dirs.append(idx)
                            number_of_possible_dirs += 1
                            # copy track for next possible way
                            new_track = Track(f"back_track_{self.back_track_idx}", track.curr_height, track.pos.copy(), track.track.copy())
                            new_track.next_step = idx
                            new_track.step()
                            self.back_track_idx += 1
                            self.track_backlog.append(new_track)
                if number_of_possible_dirs == 0:
                    track.track_status = "blocked"
                    self.blocked_count += 1
                # if list_of_dirs:
                #     self.mark_position_in_matrix(save_track_pos, list_of_dirs)

        self.tracks.clear()
        for back_track in self.track_backlog:
            if back_track.track_status in ["searching", "finished", "blocked"]:
                self.tracks.append(back_track)
        self.track_backlog.clear()
        puzzle.print_tracks()
        if self.round_counter == 244:
            pass

        if not self.tracks:
            self.print_map()
            print(f"doble:{self.doble_count} and blocked:{self.blocked_count}")
            ret_val = False

        for idx, track in enumerate(self.tracks):
            #track.step()
            if track.curr_height == "a":
                track.track_status = "finished"
                print(f"finished {len(track.track) - 1} {track}")
                ret_val = False
        #self.print_map()
        return ret_val


puzzle = Day12()
puzzle.load_puzzle_input()
puzzle.fill_map()
puzzle.find_start_point()
while 1:
    if not puzzle.find_track():
        break

puzzle.print_tracks(200)
puzzle.print_finished_track()
