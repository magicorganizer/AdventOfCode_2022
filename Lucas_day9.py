with open("input.txt") as f:
    o, o2 = 0, 0
    inp = [[int(c) for c in x.split(" ")] for x in f.readlines()]
    for l in inp:
        tria = [l]
        # part 1
        last = tria[-1]
        while any(last[i] != last[i + 1] for i in range(len(last) - 1)):
            o += last[-1]
            last = [last[i +  1] - last[i] for i in range(len(last) - 1)]
            tria.append(last)
        o += last[-1]
        print(last[-1])

        # part 2
        n = tria[-1][0]
        for t in reversed(tria[:-1]):
            n = t[0] - n
        o2 += n
    print(o, o2)