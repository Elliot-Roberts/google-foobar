import itertools


def answer(a, b):
    if b == 0:
        return [[] for _ in range(a)]
    
    key_factor = a - (b - 1)
    
    keys = 1
    while keys * key_factor % a:
        keys += 1
    
    solution = solve2(keys, key_factor, a)
    
    # initial_keys = keys
    while not solution:
        keys += 1
        # print("key:", keys)
        while keys * key_factor % a:
            keys += 1
            # print("key:", keys)
        solution = solve2(keys, key_factor, a)
    
    if solution:
        solution = [sorted(x) for x in solution]
    return solution


def solve(keys, key_factor, a, start_key=0):
    print("solving", keys, key_factor, "start", start_key)
    total_keys = keys * key_factor
    row_len = total_keys // a
    end_keys = keys - row_len
    total_end_keys = end_keys * key_factor
    sub_a = a - 1
    
    if sub_a:
        if total_end_keys % sub_a != 0:
            print("## not good A ##")
            return
    
    result = [[] for _ in range(a)]
    
    result[0] = list(range(start_key, start_key + row_len))
    
    print("ends: {} - {}".format(end_keys, list(range(start_key + row_len, start_key + keys))))
    print("space: {}, {}".format(sub_a, row_len))
    if end_keys > sub_a:
        print("----complex----")
        sub2 = solve(end_keys, key_factor, sub_a, row_len)
        
        if sub2 is None:
            print("## not good C ##")
            return

        for x in range(1, a):
            result[x] += sub2[x - 1]
        
        # print("sub2:")
        # nice_print(sub2)
        # print()
    
    else:
        end_key_set = list(range(start_key + row_len, start_key + keys))
        end_keys_full = itertools.chain.from_iterable(itertools.repeat(x, key_factor)
                                                      for x in end_key_set)
        
        for x in range(total_end_keys):
            out_i = (x % sub_a) + 1
            result[out_i].append(next(end_keys_full))
    
    nice_print(result)
    if row_len == len(result[-1]):
        return result
    
    sub = solve(row_len, key_factor - 1, sub_a, start_key)
    
    if sub is None:
        print("## not good B ##")
        return
    
    for x in range(1, a):
        result[x] += sub[x - 1]
    
    print()
    return result


def solve2(keys, key_factor, a, start_key=0, indent=0):
    print("solving", keys, key_factor, "start", start_key)
    total_keys = keys * key_factor
    row_len = total_keys // a
    end_keys = keys - row_len
    total_end_keys = end_keys * key_factor
    sub_a = a - 1
    
    if sub_a:
        if total_end_keys % sub_a != 0:
            print("## not good A ##")
            return
    
    result = [[] for _ in range(a)]
    
    result[0] = list(range(start_key, start_key + row_len))
    
    print("ends: {} - {} {}".format(end_keys, result[0], list(range(start_key + row_len, start_key + keys))))
    print("space: {}, {}".format(sub_a, row_len))
    if end_keys > sub_a:
        print("----complex----", sub_a)
        sub2 = solve2(end_keys, key_factor, sub_a, start_key + row_len, indent=indent)
        print("-end of complex-", sub_a)
        nice_print(sub2, indent)
        print("----------------")
        print()
        
        if sub2 is None:
            print("## not good C ##")
            return
        
        for x in range(1, a):
            result[x] += sub2[x - 1]

        nice_print(result, indent)
        if row_len == len(result[-1]):
            return result

        sub = solve2(row_len, key_factor - 1, sub_a, start_key, (3 * (total_end_keys // sub_a)) + indent)

        if sub is None:
            print("## not good B ##")
            return

        for x in range(1, a):
            result[x] += sub[x - 1]
        # print("sub2:")
        # nice_print(sub2)
        # print()
    
    else:
        end_key_set = list(range(start_key + row_len, start_key + keys))
        end_keys_full = itertools.chain.from_iterable(itertools.repeat(x, key_factor)
                                                      for x in end_key_set)
        
        for x in range(total_end_keys):
            out_i = (x % sub_a) + 1
            result[out_i].append(next(end_keys_full))
    
        nice_print(result, indent)
        if row_len == len(result[-1]):
            return result
        
        sub = solve2(row_len, key_factor - 1, sub_a, start_key, (3*(total_end_keys // sub_a)) + indent)
        
        if sub is None:
            print("## not good B ##")
            return
    
        for x in range(1, a):
            result[x] += sub[x - 1]
    
    print()
    return result


def nice_print(arr, indent=0):
    if isinstance(arr, list):
        for x in arr:
            print("{}{}".format(" "*indent, x))
    else:
        print("{}{}".format(" " * indent, arr))


for i in range(6, 10):
    for j in range(5, i+1):
        print("-----------------------------------", i, j)
        ans = answer(i, j)
        nice_print(ans)
        print(len(ans))
        
        if j > 1:
            for z in itertools.combinations(ans, j-1):
                if set(itertools.chain.from_iterable(z)) == set(itertools.chain.from_iterable(ans)):
                    print("////////////////////bad////////////////////")
                    nice_print(z)
                    break
        print()
