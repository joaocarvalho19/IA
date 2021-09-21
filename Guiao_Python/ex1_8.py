def sub(list,x,y):
    if list == []:
        return []

    elif list[0] == x:
        newlist = sub(list[1:],x,y)
        return [y] + newlist

    else:
        newlist = sub(list[1:],x,y)
        return [list[0]] + newlist

l = [2,1,3,1,5,6]

print(sub(l,1,8))
