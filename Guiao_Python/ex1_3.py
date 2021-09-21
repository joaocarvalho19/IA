def list_exists(list, elem):

    if list:
        if elem == list[0]:
            return True
        else:
            return list_exists(list[1:], elem)
    else:
        return False

l = [1,2,3,4,5,6]
el = 6
print(list_exists(l, el))
