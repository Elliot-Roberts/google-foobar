import itertools


def path_cost(path, states):
    costs = [states[path[x]][path[x + 1]] for x in range(len(path)-1)]
    return sum(costs)


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


def answer(tree, time):
    negatives = set((i, i2, x) for i, y in enumerate(tree) for i2, x in enumerate(y) if x < 0)
    
    betters = []
    for x in negatives:
        for i, y in enumerate(tree[x[1]]):
            if (y + x[2]) < tree[x[0]][i]:
                betters.append((x[0], x[1], i))
    
    tree_size = len(tree)
    door = tree_size - 1
    combos = [itertools.permutations(range(1, door), x) for x in range(door)]
    paths = [(0,) + x + (door,) for x in itertools.chain.from_iterable(combos)]
    
    paths = sorted(paths, key=lambda x: path_cost(x, tree), reverse=True)
    paths = sorted(paths, key=lambda x: buns(x))
    paths = sorted(paths, key=lambda x: len(buns(x)), reverse=True)
    
    for path in paths:
        new_path = path
        while path_cost(new_path, tree) > time:
            subs = subseqs(new_path, betters)
            if subs:
                new_path = insert(subs[0], new_path)
            else:
                break
        else:
            return buns(new_path)

