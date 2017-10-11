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


def answer(n):
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
