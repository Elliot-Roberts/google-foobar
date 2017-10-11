import math
import operator
from functools import reduce


def lcm(a, b):
    """
    calculates lowest common multiple of a and b
    CANNOT HANDLE 0 DENOMINATORS
    
    :param a: integer
    :param b: integer
    :return: lcm
    """
    if a > b:
        return a // math.gcd(a, b) * b
    else:
        return b // math.gcd(a, b) * a


def path_prob(path, states):
    """
    finds the simple probability of a path through states
    
    :param path: indices of states in path
    :param states: tree
    :return: numerators and denominators of probabilities in path
    """
    nums = [states[path[x]][path[x + 1]] for x in range(len(path) - 1)]  # iterates AB BC CD DE
    dens = [sum(states[x]) for x in path[:-1]]
    
    return nums, dens


def prob_condense(nums, dens):
    """
    multiplies and reduces given fractions
    CANNOT HANDLE 0 DENOMINATORS
    
    :param nums: numerators of the fractions
    :param dens: denominators of the fractions
    :return: numerator, denominator
    """
    num = reduce(operator.mul, nums)
    den = reduce(operator.mul, dens)
    
    _gcd = math.gcd(num, den)
    
    return num // _gcd, den // _gcd


def prob_combine(nums, dens):
    """
    adds list of probabilities together
    CANNOT HANDLE 0 DENOMINATORS
    
    :param nums: numerators of probabilities
    :param dens: denominators of probabilities
    :return: numerator, denominator
    """
    den = reduce(lcm, dens)
    num = sum([(den // dens[x]) * nums[x] for x in range(len(nums))])
    
    _gcd = math.gcd(num, den)
    
    return num // _gcd, den // _gcd


def explore(tree, terminals):
    """
    explores a tree and returns all paths to terminal points while avoiding loops
    
    :param tree: tree to evaluate
    :param terminals: terminal nodes of the tree
    :return: tuple of the paths found
    """
    alternates = []
    cur_path = []
    node = 0
    
    basics = []
    
    while True:
        
        if node in terminals:
            cur_path.append(node)
            basics.append(cur_path)
            
            if alternates:
                alt = alternates[-1]
                del alternates[-1]
                node = alt[1]
                cur_path = alt[0]
            else:
                break
        
        elif node in cur_path:
            # loop found
            if alternates:
                alt = alternates[-1]
                del alternates[-1]
                node = alt[1]
                cur_path = alt[0]
            else:
                break
        
        else:
            cur_path.append(node)
            choices = [(cur_path[:], i) for i, x in enumerate(tree[node]) if x != 0]
            alternates += choices[:-1]
            node = choices[-1][1]
    
    return basics


def answer(states):
    """
    evaluates probabilities in given tree, excluding loops

    :param states: probability tree represented as 2D array
    """
    # remove the chances that a state will stay the same (they do nothing and cause issues)
    for i in range(len(states)):
        states[i][i] = 0
    
    # get the terminal states and all paths to them
    terminals = [i for i, x in enumerate(states) if sum(x) == 0]
    basics = explore(states, terminals)
    
    # group all paths by terminal (leaving an empty list for unreachable terminals)
    grouped = {x: [y 
                   for y in basics 
                   if y[-1] == x] 
               for x in terminals}
    
    # get the total probability of each path
    grouped_basic_probs = {x: [prob_condense(*path_prob(z, states)) 
                               for z in y] 
                           for x, y in grouped.items()}
    
    # add paths of common terminals together
    answer_probs = {x: prob_combine(*zip(*y)) 
                    if y 
                    else (0, 1)  # to avoid div by zero issues
                    for x, y in grouped_basic_probs.items()}
    
    # manual zip while making sure that the terminals are in the right order
    sorted_keys = sorted(answer_probs.keys())
    nums = [answer_probs[x][0] for x in sorted_keys]
    dens = [answer_probs[x][1] for x in sorted_keys]
    
    # adjust all fractions to common denominator
    den = reduce(lcm, dens)
    result = [(den // dens[x]) * nums[x] for x in range(len(nums))]
    
    # throw out that denominator and use the sum of the numerators instead
    result.append(sum(result))
    
    return result
