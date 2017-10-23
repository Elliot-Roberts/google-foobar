buns1 = [
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]


def path_costs(path, states):
    """
    finds the simple probability of a path through states

    :param path: indices of states in path
    :param states: tree
    :return: numerators and denominators of probabilities in path
    """
    costs = [states[path[x]][path[x + 1]] for x in range(len(path) - 1)]  # iterates AB BC CD DE
    return costs


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
        
        if node in cur_path:
            # loop found
            loop_start = cur_path.index(node)
            cur_path.append(node)
            loop = cur_path[loop_start:]
            print(loop)
            print(path_costs(loop, tree))
            print()
            if sum(path_costs(loop, tree)) < 2:
                print(loop)
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


print(explore(buns1, [4]))
