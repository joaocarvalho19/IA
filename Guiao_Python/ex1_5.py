def reverse(list):

    if list:
        return [list[-1]] + reverse(list[:-1])
    else:
        return []

l = [1,2,3,4,5,6]

print(reverse(l))
