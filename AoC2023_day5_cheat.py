import re

with open("input.txt") as f:
    l = [[*map(int, (re.findall(r"\d+", x)))] for x in f.read().split("\n\n")]

    # task 1
    start = l[0]
    for maplist in l[1:]:
        tmp = []
        for elem in start:
            f = False
            for idx in range(len(maplist) // 3):
                dest, src, r = maplist[idx * 3:(idx + 1) * 3]
                if elem >= src and elem <= src + r - 1:
                    tmp.append(dest + elem - src)
                    f = True
            if not f:
                tmp.append(elem)
            start = tmp
    print(min(start))

    # task 2
    start = [(x, x + y - 1) for x,y in zip(l[0][0::2], l[0][1::2])]
    for maplist in l[1:]:
        mapped = []
        while len(start) > 0:
            src_start, src_stop = start.pop()
            f = False
            for idx in range(0, len(maplist), 3):
                dest, src, r = maplist[idx:(idx + 3)]
                new_interval = (max(src, src_start), min(src + r - 1, src_stop))
                if new_interval[0] < new_interval[1]:
                    mapped.append([dest + x - src for x in new_interval])
                    if src_start < new_interval[0]:
                        start.append((src_start, new_interval[0] - 1))
                    if src_stop > new_interval[1]:
                        start.append((new_interval[1] + 1, src_stop))
                    f = True
            if not f:
                mapped.append((src_start, src_stop))
        start = mapped

    print(min([x[0] for x in mapped]))