

def answer(num_buns, num_required):
    solution = [[] for x in range(num_buns)]
    
    num_of_each_key = num_buns - (num_required - 1)
    
    return num_of_each_key


print(answer(5, 3))
