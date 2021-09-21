def sub(lista1,lista2):

    l = lista1 + lista2

    if l == []:
        return []

    return sub([e for e in l[1:] if e <= l[0]]) + [l[0]] +\
            sub([e for e in l[1:] if e > l[0]])

l1 = [1,2,3]
l2 = [1,4,5,6]

print(sub(l1,l2))
