import itertools
import collections


def permute(num_buns, num_required, keys, num_of_each_key):
    template = [[] for x in range(num_buns)]
    
    key_set = set([x for x in range(keys)])
    
    print(key_set)
    
    full_resources = collections.Counter({x: num_of_each_key for x in key_set})
    
    keys_per_bun = (keys * num_of_each_key) // num_buns
    
    template[0] = [x for x in range(keys_per_bun)]
    
    return 1

def answer(num_buns, num_required):
    template = [[] for x in range(num_buns)]
    
    num_of_each_key = num_buns - (num_required - 1)
    
    keys = 1
    while keys * num_of_each_key % num_buns:
        keys += 1
    
    attempt = permute(num_buns, num_required, keys, num_of_each_key)
    
    while not attempt:
        keys *= 2
        attempt = permute(num_buns, num_required, keys, num_of_each_key)
    
    return attempt


for x in answer(5, 1):
    print(x)
