import collections as col
import itertools as it
from timeit import timeit

g = [
[1, 0, 1, 0, 0, 1, 1, 1],
[1, 0, 1, 0, 0, 0, 1, 0],
[1, 1, 1, 0, 0, 0, 1, 0],
[1, 0, 1, 0, 0, 0, 1, 0],
[1, 0, 1, 0, 0, 1, 1, 1]]
g2 = [
[1, 0, 1],
[0, 1, 0],
[1, 0, 1]]
g3 = [
[0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0]]
g4 = [
[1, 1, 0, 1, 0, 1, 0, 1, 1, 0],
[1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[0, 1, 0, 0, 0, 0, 1, 1, 0, 0]]

g5 = [[0]*9]*50

ref = [x[::-1] for x in it.product((0, 1), repeat=4)]
compat = {
    (0, 0): {0, 4, 8, 12},
    (1, 0): {1, 5, 9, 13},
    (0, 1): {2, 6, 10, 14},
    (1, 1): {3, 7, 11, 15},
}

pieces = col.defaultdict(dict)
saved_rows = col.defaultdict(dict)
single_rows = col.defaultdict(dict)

def solve_piece(options, progress):

    results = []
    if len(options) > 1:
        for x in options[0]:

            bit = ref[x]
            if progress[0] == bit[0] and progress[1] == bit[2]:

                lookup = pieces[options[1:]].get((bit[1], bit[3]))
                if lookup:
                    results += [(progress[1],) + x for x in lookup]
                else:
                    found = solve_piece(options[1:], (bit[1], bit[3]))

                    pieces[options[1:]][(bit[1], bit[3])] = found
                    results += [(progress[1],) + x for x in found]
    else:
        for x in options[0]:
            bit = ref[x]
            if progress[0] == bit[0] and progress[1] == bit[2]:
                results.append(bit[2:])
    return results


def solve_row(options, restrict):
    options = [set(x) for x in options]
    if restrict:
        for i in range(len(options)):
            options[i].intersection_update(compat[restrict[i:i+2]])

    options = tuple([frozenset(x) for x in options])

    results = []
    if len(options) > 1:
        for x in options[0]:
            bit = ref[x]
            progress = (bit[1], bit[3])
            lookup = pieces[options[1:]].get(progress)
            if lookup:
                results += [(bit[2],) + x for x in lookup]
            else:
                found = solve_piece(options[1:], progress)
                pieces[options[1:]][progress] = found
                results += [(bit[2],) + x for x in found]
    else:
        results = [ref[x][2:] for x in options[0]]

    return col.Counter(results)


def solve_all(options, cur, cnt):
    new_rows = None
    new_cnt = saved_rows[options[cur[0]:]].get(cur[1])
    if new_cnt is not None:
        return new_cnt*cnt
    else:
        lookup = single_rows[options[cur[0]]].get(cur[1])
        if lookup:
            new_rows = lookup
        else:
            new_rows = solve_row(options[cur[0]], cur[1])
            single_rows[options[cur[0]]][cur[1]] = new_rows

        next_r = cur[0] + 1

        if next_r == len(options):
            return sum(new_rows.values())*cnt

        total = 0
        for x in new_rows.items():
            total += solve_all(options, (next_r, x[0]), x[1])

        saved_rows[options[cur[0]:]][cur[1]] = total
        return total*cnt


def answer(arr):
    if len(arr[0]) > len(arr):
        print("transposing: ({0}, {1}) --> ({1}, {0})".format(len(arr), len(arr[0])))
        arr = list(zip(*arr))

    rows = len(arr)
    columns = len(arr[0])
    # for i in enumerate(ref): print(*i)

    options = [[set() for y in x] for x in arr]
    for x in range(rows):
        for y in range(columns):
            if arr[x][y]:
                options[x][y].update([1, 2, 4, 8])
            else:
                options[x][y].update([0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15])

                if x > 0:
                    if arr[x-1][y]:
                        options[x][y].difference_update([3, 7, 11, 15])

                if y > 0:
                    if arr[x][y-1]:
                        options[x][y].difference_update([5, 7, 13, 15])

                if x < rows-1:
                    if arr[x+1][y]:
                        options[x][y].difference_update([12, 13, 14, 15])

                if y < columns-1:
                    if arr[x][y+1]:
                        options[x][y].difference_update([10, 11, 14, 15])

            options[x][y] = frozenset(options[x][y])
        options[x] = tuple(options[x])
    options = tuple(options)

    total = 0
    stack = col.Counter()
    hist = 1

    new_rows = solve_row(options[0], None)
    if rows > 1:
        stack.update({(1, x[0]):x[1] for x in new_rows.items()})
    else:
        return sum(new_rows.values())

    for cur, cnt in stack.items():
        total += solve_all(options, cur, cnt)

    return total


# print(timeit("answer(g4)", number=10, globals=globals()))
print(answer(g3))

