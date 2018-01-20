import collections as col
import itertools as it

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
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0]]


def solve_piece(options, progress, length):
    if len(progress[0]) > length:
        return [tuple(progress[1])]

    ref = [x[::-1] for x in it.product((0, 1), repeat=4)]
    
    results = []
    for x in options[0]:
        bit = ref[x]
        if progress[0][-1] == bit[0] and progress[1][-1] == bit[2]:
            results += solve_piece(options[1:],
                                   [progress[0] + [bit[1]], progress[1] + [bit[3]]],
                                   length)
    return results


def solve_row(options, restrict):
    compat = {
        (0, 0): {0, 4, 8, 12},
        (1, 0): {1, 5, 9, 13},
        (0, 1): {2, 6, 10, 14},
        (1, 1): {3, 7, 11, 15},
    }
    options = [x.copy() for x in options]
    if restrict:
        for i in range(len(options)):
            options[i].intersection_update(compat[restrict[i:i+2]])

    ref = [x[::-1] for x in it.product((0, 1), repeat=4)]
    
    results = []
    for x in options[0]:
        bit = ref[x]
        progress = [list(bit[:2]), list(bit[2:])]
        results += solve_piece(options[1:], progress, len(options))
    
    return results


def answer(arr):
    if len(arr[0]) > len(arr):
        print("transposing: ({0}, {1}) --> ({1}, {0})".format(len(arr), len(arr[0])))
        arr = list(zip(*arr))
    
    rows = len(arr)
    columns = len(arr[0])
    
    ref = [x[::-1] for x in it.product((0, 1), repeat=4)]
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
                
    # for i in options: print(i)
    total = 0
    stack = [(0, None)]
    while len(stack) > 0:
        cur = stack.pop()
        new_rows = solve_row(options[cur[0]], cur[1])
        next_row = cur[0] + 1
        if next_row < rows:
            stack += [(next_row, x) for x in new_rows]
        else:
            total += len(new_rows)
    
    print(total)
    

answer(g3)