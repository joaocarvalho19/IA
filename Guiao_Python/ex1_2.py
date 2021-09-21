def list_sum(list):

    if list:
        return list[0] + list_sum(list[1:])
    else:
        return 0


l = [1,2,3]
print(list_sum(l))
