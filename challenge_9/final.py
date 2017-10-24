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


def paths_between(a, b, nodes):
    middles = [n for n in nodes if not n in (a, b)]
    mid_l = len(middles) + 1
    perms = itertools.chain.from_iterable(itertools.permutations(middles, x) for x in range(mid_l))
    return ((a,) + x + (b,) for x in perms)


def path_cost(path, states):
    costs = [states[path[x]][path[x + 1]] for x in range(len(path)-1)]
    return sum(costs)


def subseqs(a, betters):
    subs = []
    for x in betters:
        if x[0] == x[-1]:
            if x[0] in a:
                subs.append(x)
        else:
            for y in range(len(a)-1):
                if a[y:y+2] == (x[0], x[-1]):
                    subs.append(x)
                    break
    return subs


def insert(a, b):
    if a[0] == a[-1]:
        pos = b.index(a[0])
        return b[:pos] + a + b[pos+1:]
    else:
        ends = (a[0], a[-1])
        pos = next(x+1 for x in range(len(b)-1) if b[x:x+2] == ends)
        return  b[:pos-1] + a + b[pos+1:]


def buns(path):
    end = path[-1]
    return sorted(list(set(x-1 for x in path[1:] if x != end)))


def answer(tree, time):
    tree_size = len(tree)
    door = tree_size - 1
    
    pairs = itertools.permutations(range(tree_size), 2)
    
    full_set = list(range(tree_size))
    bun_set = full_set[1:-1]
    
    betters = [min(paths_between(*x, full_set), key=lambda y: path_cost(y, tree))
               for x in pairs]
    
    betters = [x for x in betters if len(x) > 2]
    
    print(betters)
    
    for x in betters:
        print("{} vs {}: {} -> {}".format((x[0], x[-1]), x, path_cost((x[0], x[-1]), tree), path_cost(x, tree)))
    combos = [itertools.permutations(range(1, door), x) for x in range(door)]
    paths = [(0,) + x + (door,) for x in itertools.chain.from_iterable(combos)]
    
    paths = sorted(paths, key=lambda x: path_cost(x, tree), reverse=True)
    paths = sorted(paths, key=lambda x: buns(x))
    paths = sorted(paths, key=lambda x: len(buns(x)), reverse=True)
    
    print()
    for x in paths: print(x)
    
    for path in paths:
        new_path = path
        while path_cost(new_path, tree) > time:
            subs = subseqs(new_path, betters)
            if subs:
                new_path = insert(subs[0], new_path)
            else:
                break
        else:
            
            print()
            print(new_path)
            return buns(new_path)



print(answer(*buns3))
