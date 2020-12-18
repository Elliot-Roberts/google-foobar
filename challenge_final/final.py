"""
########################
# concept of challenge #
########################

going forward in time, matricies evolve like so:

t=0                  t=1
┌───────────┐        ┌─────────┐
│ 1 0 0 1 1 │        │ 0 1 0 0 │
│ 1 0 1 1 1 │  --->  │ 0 0 0 0 │
│ 0 1 0 0 0 │        │ 1 0 1 1 │
│ 0 0 1 0 1 │        └─────────┘
└───────────┘

the matrix at t=1 is created based on t=0 using the following set of rules:

for every overlapping square of 2x2 values in t=0, if the square contains 
a single positive value, then the position in the t=1 matrix is positive, 
otherwise it is negative.

squares that result in a positive:
┌─────┐┌─────┐┌─────┐┌─────┐
│ 1 0 ││ 0 1 ││ 0 0 ││ 0 0 │
│ 0 0 ││ 0 0 ││ 1 0 ││ 0 1 │
└─────┘└─────┘└─────┘└─────┘

squares that result in a negative:
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│ 0 0 ││ 1 1 ││ 1 0 ││ 0 1 ││ 1 1 ││ 1 0 ││ 0 1 ││ 1 1 ││ 0 0 ││ 1 0 ││ 0 1 ││ 1 1 │
│ 0 0 ││ 0 0 ││ 1 0 ││ 1 0 ││ 1 0 ││ 0 1 ││ 0 1 ││ 0 1 ││ 1 1 ││ 1 1 ││ 1 1 ││ 1 1 │
└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘

╔t=0════════════════════╗     square has more than one positive
║ 1    0 │  0    1    1 ║            ┌t=1───────────────┐
║        │              ║    --->    │[0]   -    -    - │
║ 1    0 │  1    1    1 ║            │                  │
║────────┘              ║            │ -    -    -    - │
║ 0    1    0    0    0 ║            │                  │
║                       ║            │ -    -    -    - │
║ 0    0    1    0    1 ║            └──────────────────┘
╚═══════════════════════╝
the squares overlap like so:
╔t=0════════════════════╗        square has a single positive
║ 1  │ 0 :  0 │  1    1 ║            ┌t=1───────────────┐
║    │   :    │         ║    --->    │ 0   [1]   -    - │
║ 1  │ 0 :  1 │  1    1 ║            │                  │
║----└────────┘         ║            │ -    -    -    - │
║ 0    1    0    0    0 ║            │                  │
║                       ║            │ -    -    -    - │
║ 0    0    1    0    1 ║            └──────────────────┘
╚═══════════════════════╝
the second row:
╔t=0════════════════════╗
║ 1    0    0    1    1 ║            ┌t=1───────────────┐
║────────┐              ║            │ 0    1    0    0 │
║ 1    0 │  1    1    1 ║            │                  │
║        │              ║    --->    │[0]   -    -    - │
║ 0    1 │  0    0    0 ║            │                  │
║────────┘              ║            │ -    -    -    - │
║ 0    0    1    0    1 ║            └──────────────────┘
╚═══════════════════════╝
completed t=1:
╔t=0════════════════════╗
║ 1    0    0    1    1 ║            ┌t=1───────────────┐
║                       ║            │ 0    1    0    0 │
║ 1    0    1    1    1 ║            │                  │
║              ┌────────║            │ 0    0    0    0 │
║ 0    1    0  │ 0    0 ║            │                  │
║              │        ║    --->    │ 1    0    1   [1]│
║ 0    0    1  │ 0    1 ║            └──────────────────┘
╚═══════════════════════╝

for every t=0, there is only one t=1, but every t=1 has multiple previous
states from which it could have originated.
        ┌─────┐                   ┌───┐
the t=0 │ 0 1 │ has only one t=1: │ 0 │
        │ 1 1 │                   └───┘
        └─────┘
             ┌───┐
but that t=1 │ 0 │ could have come from any of 12 t=0s.
             └───┘
                              ┌─────────┐
                              │ 0 1 0 0 │
the t=1 in the example before │ 0 0 0 0 │ has 134 possible t=0s.
                              │ 1 0 1 1 │
                              └─────────┘

the purpose of the function is to count the number of possible t=0s for a given t=1
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

i would have liked to use a tidy mathematical way of detetmining the number, 
but didn't find one. the method used here is a glorified brute force algorithm 
that has been modified to be as efficient as possible using 'dynamic programming' 
techniques, namely 'memoization'.

memoization is the practice of saving the results of repeated operations in an 
algorithm to avoid unnecessarily redoing time-costly work. in order to apply it 
to the problem, an algorith that involves commonly occuring/repeating sub-tasks 
is needed.

"""

import collections as col
import itertools as it

"""
reference for every possible 2x2 square:

0: 0 0  1: 1 0  2: 0 1  3: 1 1  4: 0 0  5: 1 0  6: 0 1  7: 1 1  8: 0 0  ...  15: 1 1
   0 0     0 0     0 0     0 0     1 0     1 0     1 0     1 0     0 1  ...      1 1
"""
ref = [x[::-1] for x in it.product((0, 1), repeat=4)]

"""
squares in ref that have that key on top:

(0, 0): 0 0   0 0   0 0   0 0
        0 0,  1 0,  0 1,  1 1

(1, 0): 1 0   1 0   1 0   1 0
        0 0,  1 0,  0 1,  1 1

(0, 1): 0 1   0 1   0 1   0 1
        0 0,  1 0,  0 1,  1 1

(1, 1): 1 1   1 1   1 1   1 1
        0 0,  1 0,  0 1,  1 1
"""
compat = {
    (0, 0): {0, 4, 8, 12},
    (1, 0): {1, 5, 9, 13},
    (0, 1): {2, 6, 10, 14},
    (1, 1): {3, 7, 11, 15},
}

pieces = col.defaultdict(dict)  # where solutions for parts of rows are stored
saved_rows = col.defaultdict(dict)  # where solutions for combinations of rows are stored
single_rows = col.defaultdict(dict)  # where solutions for single rows are stored

def solve_piece(options, progress):
    """
    recursive function used to find all solutions for a single row.
    works by calling itself for all possible pieces at its current stage.
    works left to right, passing the right side of a possible piece, and
    the possibilites for all pieces left to go.
    when the end of a row is reached, the end pieces are returned.
    when not at the end of a row, when all calls have returned, the
    `progress` half-piece is added to every returned value and then all
    are returned. 
    the returned representations of found possible rows are just the 
    bottom half of the row of squares, because the top row is assumed 
    since squares not compatable with the row above are removed from 
    `options` beforehand, and the bottom row is needed for restricting 
    the row below.

    :param options: possible configurations for each piece in the row
    :param progress: section of the row already set
    """
    
    """
    in the process of solving example row [1, 0, 1], a possibility for 
    the first square is chosen by `solve_row()` and the right half of 
    the possible square is sent via the `progress` argument.
    
    full set of options for square 0:   {1, 2, 4, 8}
    
    possible chosen square:   2: 0 1
                                 0 0
    
    right half:   [ 1
                    0 ]
    
    
    an example `progress` argument could be:
        
        (1, 0)    <-- right half of chosen square (ref[2])
    
    
    and an example `options`:
        
        [
            
            {0, 3, 6, 9},   <-- set of options for square 1
            
            {1, 2, 4, 8}    <-- set of options for square 2
        
        ]
        
    
    next, the function iterates over the possibilites for the next 
    square and calls itself on squares compatable with `progress`, 
    passing on a subset of `options` containing the possibilities 
    for square 2:
    
    squares that are compatable with the example `progress` will look
    like so:┌──────┐, where (x)s are any values.
            │ 1  x │
            │ 0  x │
            └──────┘
    the compatability is needed because in possible t=1 matricies,
    the squares in the row overlap:
    
    square 0: ═
    square 1: ┄
    ╔═══╤┄═┄╥┄┄┄┐
    ║ 0 ┆ 1 ║ 0 ┆
    ║ 0 ┆ 0 ║ 1 ┆
    ╚═══╧═┄═╨┄┄┄┘
    
    loop over options for square 1:  {0, 3, 6, 9}
    
    -
        ref[0]: 0 0   <- not compatable
                0 0
                ^
    -
        ref[3]: 1 1   <- good. call:  solve_piece([{1, 2, 4, 8}], (1, 0))
                0 0
                ^
    -
        ref[6]: 0 1   <- not compatable
                1 0
                ^
    -
        ref[9]: 1 0   <- good. call:  solve_piece([{1, 2, 4, 8}], (0, 1))
                0 1
                ^
    endloop
    
    
    at places where a call would happen, the function first checks to see
    whether the particular combination of paramaters has been processed 
    before and had their solutions stored. if so, the call is not needed.
    
    
    if this call of `solve_piece()` was on the last square in the row, 
    the bottom half of compatable configurations for the final square 
    are returned. for example if the function is called like so:
    
    solve_piece(
        options  = [{1, 2, 4, 8}], 
        progress = (0, 1)
    )
    
    there is only one set in `options` so the function must be on the last
    square in the row.
    
    the only compatable square out of those in `options` is ref[4]:
        
        progress: [ 0       ref[4]: 0 0
                    1 ]             1 0
    
    so the returned list is:    [(1, 0)]   <-- the bottom half of ref[4]
    
    
    when the current square is not the final in the row, sub-pieces 
    returned by calls to `solve_piece()` from this function are collected, 
    then the second value of `progress` (which is the value in the bottom 
    left of the current square, and the bottom right of the previous 
    square) is added to them, and finally they are returned.
    
                                  previous square: ═
                                   current square: ┄
                       second value of `progress`: b
    colleted sub piece from `solve_piece()` calls: (c, c)
                           piece in returned list: (b, c, c)
                     bit decided in `solve_row()`: a
    a full row solution returned by `solve_row()`: (a, b, c, c)
                      no longer needed top values: *
    ╔═══╤---╥---┐
    ║ * ┆ * ║ * ┆ * :
    ║ a ┆ b ║ c ┆ c :
    ╚═══╧---╨---┘
    
    
    diagram of the recursive process of solving a row with parameters:
        
         options = [{0, 3, 6, 9}, {1, 2, 4, 8}]
        
        progress = (0, 1)
    
        
    conceptually, when called with these parameters, the function is 
    exploring all potential first rows with ref[8] as the first square. 
    here is a representation:
    
    values left to solve: x
    ┌─────────┐
    │ 0 0 x x │
    │ 0 1 x x │
    └─────────┘
    
    
    and in the bigger picture, the rest of the puzzle:
    ┌──────────────────────┐
    │ ┌------------------┐ │
    │ ┆ 0    0    x    x ┆ │
    │ ┆                  ┆ │
    │ ┆ 0    1    x    x ┆ │
    │ └------------------┘ │
    │   x    x    x    x   │
    │                      │
    │   x    x    x    x   │
    │                      │
    └──────────────────────┘
    
    the function finds that there is only one possible configuration of
    the first row when the first square is ref[8]
    
    [
        [[0, 0, 1, 0],
         [0, 1, 0, 0]]
    ]
    
    """
    results = []  # list to store found compatable pieces
    if len(options) > 1:  # the function is not on the last peice in the row
        for x in options[0]:  # iterate over possibilities for the current piece
            bit = ref[x]  # fetch square from ref
            
            if progress[0] == bit[0] and progress[1] == bit[2]:  # the square fits the progress
                lookup = pieces[options[1:]].get((bit[1], bit[3]))  # fetch stored solutions
                # `.get()` returns `None` if the key is not in the dictionary
                if lookup:  # stored solutions were found
                    # add solutions to result with progress piece added to each
                    results += [(progress[1],) + x for x in lookup]
                else:  # no stored solutions were found
                    found = solve_piece(options[1:], (bit[1], bit[3]))  # get solutions

                    pieces[options[1:]][(bit[1], bit[3])] = found  # save found solutions
                    # add the found solutions to result with progress piece added to each
                    results += [(progress[1],) + x for x in found]
    else:  # the function is on the last piece
        for x in options[0]:
            bit = ref[x]
            if progress[0] == bit[0] and progress[1] == bit[2]:
                results.append(bit[2:])  # add piece to the results
    return results


def solve_row(options, restrict):
    """
    gets all possible solutions for a row when restricted by `restrict`
    
    :param options: possible configurations for each piece in the row
    :param restrict: set of bits from the row above
    """
    
    """
    this section prepairs the options for the solve piece function - 
    removes options that conflict with `restrict` (so that all found
    solutions will be valid)
    """
    if restrict:  # the row is restricted by a row above it
        options = [set(x) for x in options]  # make options mutable
        for i in range(len(options)):  # iterate over indicies of `options`
            # remove pieces not compatable with `restrict`
            options[i].intersection_update(compat[restrict[i:i+2]])
        options = tuple([frozenset(x) for x in options])  # make options immutable
        # the options are used as keys in dicts so need to be immutable
    
    """this section runs the solve piece function - gets the possible rows"""
    results = []  # stores found solutions
    if len(options) > 1:  # the row is more than one piece
        for x in options[0]:  # iter over options for the first piece
            bit = ref[x]  # get square
            progress = (bit[1], bit[3])  # set piece for exploration
            lookup = pieces[options[1:]].get(progress)  # lookup stored results
            if lookup:  # stored results were found (i.e. state has been solved before)
                results += [(bit[2],) + y for y in lookup]  # update solutions
            else:  # state has never been solved
                found = solve_piece(options[1:], progress)  # solve row (with piece `x` set)
                pieces[options[1:]][progress] = found  # save state and solutions
                results += [(bit[2],) + y for y in found]  # update solutions
    else:  # the row is a single piece
        results = [ref[x][2:] for x in options[0]]  # update solutions

    return col.Counter(results)  # return the found rows as a counter


def solve_all(options, cur, cnt):
    """
    recursive function that solves combinations of rows.
    it stores and returns only counts of rows since no further
    work needs to be done with them
    
    :param options: potential pieces in given rows
    :param cur: tuple -> (current row number, resctricting row above)
    :param cnt: multiplier for total (simulating solving multiple at once)
    """
    
    # fetch solution count for the rest of the rows
    new_cnt = saved_rows[options[cur[0]:]].get(cur[1])
    if new_cnt is not None:  # a stored count was found
        return new_cnt*cnt  # return count
    else:  # the current state has not been solved before
        lookup = single_rows[options[cur[0]]].get(cur[1])  # fetch solutions for current single row
        if lookup:  # stored solutions were found
            new_rows = lookup  # use stored solutions for further solving
        else:  # this state (options/restrict combination) has not been solved before
            new_rows = solve_row(options[cur[0]], cur[1])  # solve for this state
            single_rows[options[cur[0]]][cur[1]] = new_rows  # store found solutions

        next_r = cur[0] + 1  # the row to be explored next is one below the current

        if next_r == len(options):  # the next row is the last row in the matrix
            return sum(new_rows.values())*cnt  # exploration is not necessary - return count

        total = 0  # count of options returned by exploration of the rest of the rows
        for x in new_rows.items():  # iter over (restrict, count of duplicates) pairs
            total += solve_all(options, (next_r, x[0]), x[1])  # call self on all found new rows

        saved_rows[options[cur[0]:]][cur[1]] = total  # save state
        return total*cnt


def answer(arr):
    """
    here assuming that speed is improved when there are more rows than columns
    transposes the matrix if necessary to make it that way
    """
    if len(arr[0]) > len(arr):  # columns are longer than rows
        arr = list(zip(*arr))  # transpose

    rows = len(arr)  # store number of rows (this is also the length of columns)
    columns = len(arr[0])  # store number of columns (this is also the length of rows)
    
    options = [[set() for y in x] for x in arr]  # empty structure for storing potential states
    for x in range(rows):  # iter over row indicies
        for y in range(columns):  # iter over column indicies
            if arr[x][y]:  # this position is positive
                # add all possible states that result in a positive
                options[x][y].update([1, 2, 4, 8])
            else:  # this position is negative
                # add all possible states that result in a positive
                options[x][y].update([0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15])
                
                """
                when a [0] in a t=1 is adjacent to a [1], since the [1] will never have two ones,
                the squares for the [0] with two ones that would overlap with the [1] in the t=0
                are not compatable and can be eliminated before further computing. for example:
                
                t=1
                ┌──────┐
                │ 0  1 │
                └──────┘
                
                before trimming, the possibilites for the [0] in t=1 are:
                [0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]
                ┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
                │ 0 0 ││ 1 1 ││ 1 0 ││ 0 1 ││ 1 1 ││ 1 0 ││ 0 1 ││ 1 1 ││ 0 0 ││ 1 0 ││ 0 1 ││ 1 1 │
                │ 0 0 ││ 0 0 ││ 1 0 ││ 1 0 ││ 1 0 ││ 0 1 ││ 0 1 ││ 0 1 ││ 1 1 ││ 1 1 ││ 1 1 ││ 1 1 │
                └─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘
                
                but it is clear to see that the squares with two ones on the right side will not
                work in a t=0, because they will overlap with the [1], and the [1] requires a square
                with only a positive value. such invalid squares in this case are:
                [10, 11, 14, 15]
                
                """
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

print(answer([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]))

