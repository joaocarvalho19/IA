def remove_e_conta(lista, elem):

    if lista:
        if lista[0] == elem:
            return remove_e_conta(lista[1:],elem)
        else:
            return [lista[0]] + remove_e_conta(lista[1:],elem)
    else:
        return []

l = [1,2,3,2,2,5,6,7]
e = 2

print(remove_e_conta(l,e))