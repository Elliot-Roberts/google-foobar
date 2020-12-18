import itertools
import numpy as np


def answer(a, b):
    """
    wrapper function for solve()
    
    :param a: number of sets
    :param b: minimum number of sets
    """
    # return empty lists if none required
    if b == 0:
        return [[] for _ in range(a)]
    
    # num of duplicates of each key among all bunnies
    key_factor = a - (b - 1)
    
    # find number of unique keys such that all sets can be made equal length
    keys = 1
    while keys * key_factor % a:
        keys += 1
    
    # try solving with this number of unique keys
    solution = solve(keys, key_factor, a)
    
    # try new numbers of keys until an answer is found
    while not solution:
        keys += 1
        while keys * key_factor % a:
            keys += 1
        solution = solve(keys, key_factor, a)
    
    # sort all the sets
    if solution:
        solution = [sorted(x) for x in solution]
    return solution


def solve(keys, key_factor, a, start_key=0):
    """
    creates `a` sets populated by keys such that any combination of `b` sets will collectively have
    all unique keys, and no combination of `b`-1 keys has this.
    
    :param keys: total number of unique keys
    :param key_factor: number of duplicates of each key
    :param a: number of sets in current solve
    :param start_key: lowest key value in current solve
    """
    # set up useful variables
    total_keys = keys * key_factor  # count of all keys in the sets including duplicates
    row_len = total_keys // a  # number of keys per set
    end_keys = keys - row_len  # number of unique keys not included in the first set
    total_end_keys = end_keys * key_factor
    sub_a = a - 1  # number of sets after the first set
    
    # return none if the keys don't fit properly
    if sub_a:
        if total_end_keys % sub_a != 0:
            return
    
    # create empty placeholder for sets
    result = [[] for _ in range(a)]
    
    # create first set as sequential numbers from the start key
    result[0] = list(range(start_key, start_key + row_len))
    
    # if there are more end keys than sets past the first set
    if end_keys > sub_a:
        # solve for the end keys
        sub2 = solve(end_keys, key_factor, sub_a, start_key + row_len)
        
        # return none if any sub-solve has failed
        if sub2 is None:
            return
        
        # add the ends sub-solve to the current solve
        for x in range(1, a):
            result[x] += sub2[x - 1]
    
    else:
        # create iterator over each end key each repeated `key_factor` times
        end_key_set = list(range(start_key + row_len, start_key + keys))
        end_keys_full = itertools.chain.from_iterable(itertools.repeat(x, key_factor)
                                                      for x in end_key_set)
        
        # use above iterator to layer keys into the current solve
        for x in range(total_end_keys):
            out_i = (x % sub_a) + 1
            result[out_i].append(next(end_keys_full))
    
    # if the last set of the current solve is as long as the first set, the solve is done
    if row_len == len(result[-1]):
        return result
    
    # else solve for the space left in the solve (using of the unused keys)
    sub = solve(row_len, key_factor - 1, sub_a, start_key)
    
    # if this sub solve fails, return none
    if sub is None:
        return
    
    # else add the sub-solve of remaining keys to the current solve
    for x in range(1, a):
        result[x] += sub[x - 1]
    
    return result


def nice_print(arr, indent=0):
    if isinstance(arr, list):
        arr = np.asarray(arr)
        print(arr)
    else:
        print("{}{}".format(" " * indent, arr))


def wew(a, b):
    nice_print(answer(a, b))

# 
# for i in range(1, 10):
#     for j in range(i + 1):
#         print("-----------------------------------", i, j)
#         ans = answer(i, j)
#         nice_print(ans)
# 
#         if j > 1:
#             for z in itertools.combinations(ans, j - 1):
#                 if set(itertools.chain.from_iterable(z)) == set(itertools.chain.from_iterable(ans)):
#                     print("////////////////////bad////////////////////")
#                     nice_print(z)
#                     break
#         print("\n")

nice_print(answer(7, 5))
