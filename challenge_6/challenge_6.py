import json
import math
import operator
from functools import reduce

prob1 = [
    [0, 1, 0, 0, 0, 1],  # s0, the initial state, goes to s1 and s5 with equal probability
    [4, 0, 0, 3, 2, 0],  # s1 can become s0, s3, or s4, but with different probabilities
    [0, 0, 0, 0, 0, 0],  # s2 is terminal, and unreachable (never observed in practice)
    [0, 0, 0, 0, 0, 0],  # s3 is terminal
    [0, 0, 0, 0, 0, 0],  # s4 is terminal
    [0, 0, 0, 0, 0, 0],  # s5 is terminal
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


def getlast(a):
    """
    gets last item of a list
    
    :param a: list
    :return: last item
    """
    return operator.getitem(a, -1)


def path_prob(path, states):
    """
    finds the simple probability of a path through states
    
    :param path: indices of states in path
    :param states: tree
    :return: fractional probability
    """
    numerator = reduce(operator.mul, [states[path[x]][path[x + 1]] for x in range(len(path) - 1)])
    denominator = reduce(operator.mul, [sum(states[x]) for x in path[:-1]])
    
    return numerator, denominator


def nice_print(item, prune=False):
    """
    was used to print some dictionaries nicely but is no longer useful
    
    :param item: dictionary or other object
    :param prune: whether to remove empty dictionary entries
    """
    if isinstance(item, dict):
        if prune:
            nice1 = {
                str(x2): {str(x1): str(y1) for x1, y1 in y2.items()}
                for x2, y2 in item.items() if y2}
        else:
            nice1 = {
                str(x2): {str(x1): str(y1) for x1, y1 in y2.items()}
                for x2, y2 in item.items()}
    else:
        nice1 = item
    
    print(json.dumps(nice1, indent=4, sort_keys=True))


def answer(states):
    """
    old function left because some parts are useful

    """
    terminals = [i for i, x in enumerate(states) if sum(x) == 0]
    basics, loops = explore(0, states, terminals)
    
    print("basics:")
    print(basics)
    print("loops:")
    print(loops)
    
    fracs = [[(states[path[x]][path[x + 1]], sum(states[path[x]])) for x in range(len(path) - 1)] for path in basics]
    
    # numerators = [states[path[x]][path[x+1]] for path in basics for x in range(len(path)-1)]
    #
    # denominators = [sum(states[x]) for path in basics for x in path]
    #
    # print(denominators)
    # print(numerators)
    
    fracs = [reduce(lambda x, y: (x[0] * y[0], x[1] * y[1]), x) for x in fracs]
    
    _lcm = reduce(lcm, [y for x, y in fracs])
    
    fracs = [(_lcm // y) * x for x, y in fracs]
    
    print()
    
    print(_lcm)
    
    print(fracs)


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


def answer2(states):
    """
    evaluates probabilities in given tree
    
    :param states: probability tree represented as 2D list
    """
    terminals = [i for i, x in enumerate(states) if sum(x) == 0]
    basics, loops = explore(0, states, terminals)
    
    loops = [((y[1], y[1] - y[0]), x) for x, y in zip(loops, (path_prob(z, states) for z in loops))]
    
    # result = []
    
    grouped = {x: [y for y in basics if getlast(y) == x] for x in terminals}
    
    print([path_prob(x, states) for x in basics])
    print(loops)
    
    # loop_groups = {x[0]: for x in loops}
    
    print(grouped)


answer2(prob1)
