def cabeca(lista):
    if lista:
        return lista[0]


l = [5,2,1,4]
l2 = []
print("Lista1: [5,2,1,4]\n","Elemento à cabeça: ",cabeca(l))
print("Lista1: []\n","Elemento à cabeça: ",cabeca(l2))