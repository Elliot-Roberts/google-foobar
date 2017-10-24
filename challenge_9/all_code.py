import operator
import itertools

buns1 = ([
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
], 1)

buns2 = ([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)


buns3 = ([
    [0, 9, 0, 9, 1],
    [0, 0, 9, 0, 1],
    [9, 9, 0, 9, 1],
    [9, 9, 9, 0,-2],
    [-1,-1,-1,-1,0],
], 1)


def path_cost(path, states):
    """
    finds the simple probability of a path through states

    :param path: indices of states in path
    :param states: tree
    :return: numerators and denominators of probabilities in path
    """
    costs = [states[path[x]][path[x + 1]] for x in range(len(path) - 1)]  # iterates AB BC CD DE
    return sum(costs)


def answer(tree, time):
    transform = list(zip(*tree))
    
    negatives = set((i, i2, x) for i, y in enumerate(tree) for i2, x in enumerate(y) if x < 0)
    
    for x in negatives:
        for i, y in enumerate(tree[x[1]]):
            if (y + x[2]) < tree[x[0]][i]:
                print(x[0], x[1], i)
    
    mins = [(x, sum(transform[x]), sum(tree[x])) for x in range(len(tree))]
    mins = sorted(mins, key=lambda x: x[1]+x[2])
    print(mins)
    return negatives
    

def subseqs(a, betters):
    subs = []
    for x in betters:
        if x[0] == x[2]:
            if x[0] in a:
                subs.append(x)
        else:
            for y in range(len(a)-1):
                if a[y:y+2] == (x[0], x[2]):
                    subs.append(x)
                    break
    return subs


def insert(a, b):
    if a[0] == a[2]:
        pos = b.index(a[0])
        return b[:pos] + a[:2] + b[pos:]
    else:
        pos = next(x+1 for x in range(len(b)-1) if b[x:x+2] == (a[0], a[2]))
        return  b[:pos] + (a[1],) + b[pos:]


def buns(path):
    end = path[-1]
    return sorted(list(set(x-1 for x in path[1:] if x != end)))


def best(stats, tree, time):
    paths = [x for x in stats if x[2] <= time]
    #paths = sorted(paths, key=buns)
    return sorted(stats, key=lambda x: len(x[1]), reverse=True)


def improve(path, betters):
    fixed = path
    subs = subseqs(path, betters)
    for sub in subs:
        fixed = insert(sub, fixed)
    return fixed
                


def answer2(tree, time):
    negatives = set((i, i2, x) for i, y in enumerate(tree) for i2, x in enumerate(y) if x < 0)
    
    betters = []
    for x in negatives:
        for i, y in enumerate(tree[x[1]]):
            if (y + x[2]) < tree[x[0]][i]:
                betters.append((x[0], x[1], i))
    
    print(betters)
    print()
    tree_size = len(tree)
    door = tree_size - 1
    combos = [itertools.permutations(range(1, door), x) for x in range(door)]
    paths = [(0,) + x + (door,) for x in itertools.chain.from_iterable(combos)]
    for x in paths:
        print(x)
    
    improved = []
    for x in paths:
        x2 = improve(x, betters)
        improved.append(x2)
    
    print()
    nice_print(improved)
    print()
    stats = [(x, buns(x), path_cost(x, tree)) for x in improved]
    stats = sorted(stats, key=lambda x: len(x[1]), reverse=True)
    thresh = next(x for x in stats if x[2] <= time)
    overs = list(itertools.takewhile(lambda x: len(x[1]) > len(thresh[1]), stats))
    improvements = []
    for x in overs:
        x = x[0]
        while path_cost(x, tree) > time:
            subs = subseqs(x, betters)
            if not subs:
                break
            else:
                for sub in subs:
                    x = insert(sub, x)
        else:
            improvements.append(x)
    
    assert not improvements
    finals = [(x, buns(x), path_cost(x, tree)) for x in improvements] + [thresh]
    print(finals)
    
    return best(finals, tree, time)[0][1]
    


def explore(tree, time):
    """
    explores a tree and returns all paths to terminal points while avoiding loops

    :param tree: tree to evaluate
    :param terminals: terminal nodes of the tree
    :return: tuple of the paths found
    """
    tree_size = len(tree)
    door = tree_size - 1
    bunnies = set(range(1, tree_size-1))
    print(bunnies)
    alternates = []
    cur_path = []
    node = 0
    
    basics = []
    
    while True:
        full_path = cur_path + [node]
        
        if node == door:
            if path_cost(full_path, tree) <= time:
                basics.append(full_path)
            
            if bunnies.issubset(cur_path):
                if alternates:
                    alt = alternates[-1]
                    del alternates[-1]
                    node = alt[1]
                    cur_path = alt[0]
                    continue
                else:
                    break
        
        if node in cur_path:
            # loop found
            #loop_start = len(cur_path) - next(i for i, x in enumerate(reversed(cur_path)) if x == node)
            loop = full_path[len(cur_path)-1:]
            #print(loop)
            #print(sum(path_cost(loop, tree)))
            #print()
            if path_cost(loop, tree) < 1:
                print(loop)
                print("costs:", path_cost(loop, tree))
                print()
            else:
                if alternates:
                    alt = alternates[-1]
                    del alternates[-1]
                    node = alt[1]
                    cur_path = alt[0]
                    continue
                else:
                    break
        
        cur_path.append(node)
        choices = [(cur_path[:], i) for i, x in enumerate(tree[node]) if x != 0]
        alternates += choices[:-1]
        node = choices[-1][1]
    
    return basics


def nice_print(arr, indent=0):
    if isinstance(arr, list):
        for x in arr:
            print("{}{}".format(" "*indent, x))
    else:
        print("{}{}".format(" " * indent, arr))


print(answer2(*buns3))
