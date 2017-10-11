from matplotlib import pyplot


def answer1(n):
    num = int(n)
    
    ops = 0
    
    while num > 1:
        print(ops, num)
        if num % 2 == 0:
            num //= 2
        else:
            num -= 1
        ops += 1
    return ops


def answer2(n):
    num = int(n)
    
    op_num = 0
    # ops = [str(num)]
    
    while num > 1:
        if num % 2 == 0:
            num //= 2
        else:
            upper_bound = 1 << (num-1).bit_length()
            dif_up = upper_bound - num
            if dif_up < num >> 1:
                num += 1
            else:
                num -= 1
        op_num += 1
        # ops.append(str(num))

    # return " -> ".join(ops), op_num
    return op_num


def tester(func):
    for x in range(1, 65):
        print(x, func(x))


def plot_test(func, start, stop):
    pyplot.plot([func(x) for x in range(start, stop)])
    pyplot.show()


def q(num):
    upper_bound = 1 << (num - 1).bit_length()
    dif_up = upper_bound - num
    return dif_up + (num & (~num+1)), (num >> 1), dif_up + (num & (~num+1)) < num >> 1


def f(num):
    upper_bound = 1 << (num - 1).bit_length()
    dif_up = upper_bound - num
    
    lower_bound = upper_bound // 2
    dif_down = num - lower_bound
    return dif_down, dif_up


def get_if_up(num):
    num += 1
    
    ops = 0
    
    while num > 1:
        if num % 2 == 0:
            num //= 2
        else:
            num -= 1
        ops += 1
    return ops


def get_if_down(num):
    num -= 1
    
    ops = 0
    
    while num > 1:
        if num % 2 == 0:
            num //= 2
        else:
            num -= 1
        ops += 1
    return ops


def inneficient(n):
    num = int(n)
    
    ops = 0
    op_nums = [str(num)]

    while num > 1:
        if num % 2 == 0:
            num //= 2
        else:
            if get_if_down(num) < get_if_up(num):
                num -= 1
            else:
                num += 1
        ops += 1
        op_nums.append(str(num))
        
    return ops, " -> ".join(op_nums)
    

tester(inneficient)
