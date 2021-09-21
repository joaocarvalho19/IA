#Exercicio 1.1
def comprimento(lista):
	if lista:
		return 1 + comprimento(lista[1:])
	else:
		return 0

#Exercicio 1.2
def soma(lista):
	if lista:
		return lista[0] + soma(lista[1:])
	else:
		return 0

#Exercicio 1.3
def existe(lista, elem):
	if lista:
		if elem == lista[0]:
			return True
		else:
			return existe(lista[1:], elem)
	else:
		return False

#Exercicio 1.2
def soma(lista):
	pass

#Exercicio 1.3
def existe(lista, elem):
	pass


#Exercicio 1.4
def concat(l1, l2):
	pass

#Exercicio 1.5
def inverte(lista):
	if lista:
		return [lista[-1]] + inverte(lista[:-1])
	else:
		return []
	pass

#Exercicio 1.6
def capicua(lista):
	pass

#Exercicio 1.7
def explode(lista):
	pass

#Exercicio 1.8
def substitui(lista, original, novo):
	if lista == []:
		return []

	if lista[0] == original:
		newlist = substitui(lista[1:],original,novo)
		return [novo] + newlist

	else:
		newlist = substitui(lista[1:],original,novo)
		return [lista[0]] + newlist

#Exercicio 1.9
def junta_ordenado(lista1, lista2):
	pass

#Exercicio 2.1
l1=[]
l2=[]
def separar(lista):
	if not lista:
		return []
	l1.append(lista[0][0])
	l2.append(lista[0][1])
	separar(lista[1:])
	return (l1,l2)

def separar(lista):
	pass

#Exercicio 2.2
def remove_e_conta(lista, elem):
	pass

#Exercicio 3.1
def cabeca(lista):
	pass

#Exercicio 3.2
def cauda(lista):
	pass

#Exercicio 3.3
def juntar(l1, l2):
    pass

#Exercicio 3.4
def menor(lista):
	pass

#Exercicio 3.6
def max_min(lista):
	pass
