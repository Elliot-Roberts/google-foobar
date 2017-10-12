def get_if_up(num):
    """
    determines number of steps required to reduce num to 1 after adding 1
    
    :param num: number to evaluate
    """
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
    """
    determines number of steps required to reduce num to 1 after subtracting 1
    
    :param num: number to evaluate
    """
    num -= 1
    
    ops = 0
    
    while num > 1:
        if num % 2 == 0:
            num //= 2
        else:
            num -= 1
        ops += 1
    return ops


def answer(n):
    """
    returns smallest number of steps (a step being any of [+1, -1, //2]) required to reduce n to 1
    this approach seems like it should be really slow, but it works...
    
    :param n: number to reduce
    """
    num = int(n)
    
    ops = 0
    
    while num > 1:
        if num % 2 == 0:
            num //= 2
        else:
            if get_if_down(num) < get_if_up(num):
                num -= 1
            else:
                num += 1
        ops += 1
    
    return ops
