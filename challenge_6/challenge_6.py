import math
import operator
from functools import reduce
from timeit import timeit

# good
m = [
    [0, 1, 0, 0, 0, 1],
    [4, 0, 0, 3, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# good
prob1 = [
    [0, 1, 0, 0, 0, 1],  # s0, the initial state, goes to s1 and s5 with equal probability
    [4, 0, 0, 3, 2, 0],  # s1 can become s0, s3, or s4, but with different probabilities
    [0, 0, 0, 0, 0, 0],  # s2 is terminal, and unreachable (never observed in practice)
    [0, 0, 0, 0, 0, 0],  # s3 is terminal
    [0, 0, 0, 0, 0, 0],  # s4 is terminal
    [0, 0, 0, 0, 0, 0],  # s5 is terminal
]

# good
prob2 = [
    [0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# good
prob3 = [
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# good
prob6 = [
    [0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# TODO solve these ones:
prob4 = [
    [7, 0, 0, 0, 0, 3, 2, 5, 0, 0],
    [0, 6, 0, 3, 0, 0, 0, 7, 0, 0],
    [0, 0, 5, 0, 0, 0, 0, 3, 0, 0],
    [9, 0, 0, 5, 0, 0, 7, 0, 5, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 8, 0, 8, 0, 0],
    [0, 0, 7, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

prob5 = [
    [1, 1, 0, 3, 0, 7],
    [0, 2, 4, 0, 0, 1],
    [0, 0, 3, 5, 3, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]


def lcm(a, b):
    """
    calculates lowest common multiple of a and b
    
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
    nums = [states[path[x]][path[x + 1]] for x in range(len(path) - 1)]
    dens = [sum(states[x]) for x in path[:-1]]
    
    return nums, dens


def prob_condense(nums, dens):
    """
    multiplies and reduces given fractions
    
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
    
    :param nums: numerators of probabilities
    :param dens: denominators of probabilities
    :return: numerator, denominator
    """
    den = reduce(lcm, dens)
    num = sum([(den // dens[x]) * nums[x] for x in range(len(nums))])
    
    _gcd = math.gcd(num, den)
    
    return num // _gcd, den // _gcd


def loop_prob_effect(num, den):
    """
    calculates infinite sum of n=0 (num/den)^n n->inf
    
    :param num: numerator
    :param den: denominator
    :return: numerator, denominator
    """
    return den, den - num


def explore(node, tree, terminals):
    """
    explores a tree and returns all paths to terminal points as well as identifies loops
    
    :param node: current node being evaluated
    :param tree: tree to evaluate
    :param terminals: terminal nodes of the tree
    :return: tuple of the paths and loops found respectively
    """
    alternates = []
    cur_path = []
    
    basics = []
    loops = []
    
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
            cur_path.append(node)
            loops.append(cur_path)
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
    
    return basics, loops


def answer(states):
    """
    evaluates probabilities in given tree
    
    :param states: probability tree represented as 2D list
    """
    terminals = [i for i, x in enumerate(states) if sum(x) == 0]
    basics, loops = explore(0, states, terminals)
    
    loop_probs = [(set(x), loop_prob_effect(*prob_condense(*path_prob(x, states)))) for x in loops]
    
    grouped = {x: [y for y in basics if y[-1] == x] for x in terminals}
    
    grouped_basic_probs = {x: [prob_condense(*path_prob(z, states)) for z in y] for x, y in grouped.items()}
    
    if loops:
        grouped_loop_probs = {x: [prob_condense(*zip(*(w[1] for w in loop_probs if w[0].intersection(z)))) for z in y]
                              for x, y in grouped.items()}
    
        answer_probs = {x: (prob_combine(*list(zip(*[prob_condense(*zip(*y))
                                                     for y in zip(grouped_basic_probs[x], grouped_loop_probs[x])])))
                            if grouped[x] else (0, 1))  # (0, 1) to avoid division by zero problems in calculations
                        for x in terminals}
    else:
        answer_probs = {x: prob_combine(*zip(*y)) if y else (0, 1) for x, y in grouped_basic_probs.items()}
    
    # for i in answer_probs.items():
    #     print("{}: {}".format(*i))
    
    nums = [answer_probs[x][0] for x in sorted(answer_probs.keys())]
    dens = [answer_probs[x][1] for x in sorted(answer_probs.keys())]
    
    den = reduce(lcm, dens)
    result = [(den // dens[x]) * nums[x] for x in range(len(nums))]
    
    # print(den - sum(result))
    
    result.append(den)
    
    # print(result)
    return result


print(timeit('answer(prob1)', globals=globals(), number=10000))
answer(prob4)
