def capicua(lista):


    if lista==[]:
        return []
    inv = capicua(lista[1:])
    print(inv)
    inv.append(lista[0])
    if inv == lista:
        print(True)
        return inv
    else:
        print(False)
        return inv


l = [1,2,3,3,2,1]

print(capicua(l))
