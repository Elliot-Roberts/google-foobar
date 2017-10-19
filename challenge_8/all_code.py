import itertools
import collections
from json import dumps


def solve(keys, key_factor, a):
    
    total_keys = keys * key_factor
    row_len = total_keys // a
    end_keys = keys - row_len
    total_end_keys = end_keys * key_factor
    sub_a = a-1
    
    if sub_a == 0:
        return [[0]]
    
    if total_end_keys % sub_a != 0:
        return
    
    key_set = list(range(keys))
    result = [[] for x in range(a)]
    
    new_key_factor = key_factor - 1
    
    result[0] = list(range(row_len))
    
    end_key_set = list(range(row_len, keys))
    end_keys_full = itertools.chain.from_iterable(itertools.repeat(x, key_factor) 
                                                  for x in end_key_set)
    for x in range(total_end_keys):
        out_i = (x % sub_a) + 1
        result[out_i].append(next(end_keys_full))
    
    if row_len == len(result[-1]):
        return result
    
    sub = solve(row_len, key_factor-1, sub_a)
    
    if sub == None:
        return
    
    for x in range(1, a):
        result[x] += sub[x-1]
    
    return result


def solve2(keys, key_factor, a, indent=0):
    
    total_keys = keys * key_factor
    row_len = total_keys // a
    end_keys = keys - row_len
    total_end_keys = end_keys * key_factor
    sub_a = a-1
    
    if sub_a == 0:
        return [[0]]
    
    if total_end_keys % sub_a != 0:
        print("bad - {}, {}".format(total_end_keys, sub_a))
        print()
        return
    
    key_set = list(range(keys))
    result = [[] for x in range(a)]
    
    new_key_factor = key_factor - 1
    
    result[0] = list(range(row_len))
    
    end_key_set = list(range(row_len, keys))
    end_keys_full = itertools.chain.from_iterable(itertools.repeat(x, key_factor) 
                                                  for x in end_key_set)
    
    for x in range(total_end_keys):
        out_i = (x % sub_a) + 1
        result[out_i].append(next(end_keys_full))
    
    for x in result:
        print("{}{}".format(" "*indent, x))
    if row_len == len(result[-1]):
        return result
    
    sub = solve2(row_len, key_factor-1, sub_a, (3*(total_end_keys // sub_a)) + indent)
    
    if sub == None:
        return
    
    for x in range(1, a):
        result[x] += sub[x-1]
    
    return result


def answer(a, b):
    
    key_factor = a - (b - 1)
    
    keys = 1
    while keys * key_factor % a:
        keys += 1
    
    solution = None
    
    initial_keys = keys
    while not solution:
        solution = solve2(keys, key_factor, a)
        keys += initial_keys
    
    if solution:
        solution = [sorted(x) for x in solution]
    print()
    return solution


for x in answer(5, 3):
    print(x)
