import itertools
import operator


def path_costs(path, states):
    costs = [states[path[x]][path[x + 1]] for x in range(len(path) - 1)]  # iterates AB BC CD DE
    return costs


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
    return sorted([x - 1 for x in path[1:] if x != end])


def best(stats, time):
    stats = [x for x in stats if x[2] <= time]
    stats = sorted(stats, key=operator.itemgetter(1))
    return sorted(stats, key=lambda x: len(x[1]), reverse=True)


def improve(path, betters):
    fixed = path
    subs = subseqs(path, betters)
    for sub in subs:
        fixed = insert(sub, fixed)
    return fixed


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
    
    improved = []
    for x in paths:
        x2 = improve(x, betters)
        improved.append(x2)
    
    stats = [(x, buns(x), sum(path_costs(x, tree))) for x in improved]
    stats = sorted(stats, key=lambda x: len(x[1]), reverse=True)
    thresh = next(x for x in stats if x[2] <= time)
    overs = list(itertools.takewhile(lambda x: len(x[1]) > len(thresh[1]), stats))
    improvements = []
    for x in overs:
        x = x[0]
        while sum(path_costs(x, tree)) > time:
            subs = subseqs(x, betters)
            if not subs:
                break
            else:
                for sub in subs:
                    x = insert(sub, x)
        else:
            improvements.append(x)
    
    finals = [(x, buns(x), sum(path_costs(x, tree))) for x in improvements] + [thresh]
    
    return best(finals, time)[0][1]

