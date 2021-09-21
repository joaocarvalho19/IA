

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return my_list2string(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))
    
    def list_associations(self):
        names=[d.relation.name for d in self.declarations if isinstance(d.relation,Association)]
        return list(set(names))

    def list_objects(self):
        ins=[s.relation.entity1 for s in self.declarations if isinstance(s.relation,Subtype)]
        return list(set(ins))
    
    def list_users(self):
        users=[d.user for d in self.declarations]
        return list(set(users))

    def list_types(self):
        ty=[s.relation.entity2 for s in self.declarations if isinstance(s.relation,Member) or isinstance(s.relation,Subtype)]
        return list(set(ty))

    def list_local_associations(self,ent):
        rels = [a.relation for a in self.declarations if isinstance(a.relation,Association)]
        final_assoc = []
        for i in rels:
            if (i.entity1 == ent or i.entity2 == ent):
                if i.name not in final_assoc:
                    final_assoc.append(i.name)
        return final_assoc

    def list_relations_by_user(self,u):
        rel_names=[]
        for d in self.declarations:
            if d.user == u and d.relation.name not in rel_names:
                rel_names.append(d.relation.name)
        print(rel_names)
        return rel_names

    def list_local_associations_by_user(self,ent):
        rels = [a for a in self.declarations if isinstance(a.relation,Association)]
        list_assoc=[]
        for i in rels:
            if (i.relation.entity1 == ent or i.relation.entity2 == ent) and (i.relation.name, i.user) not in list_assoc:
                list_assoc.append((i.relation.name, i.user))
        return list_assoc

# Funcao auxiliar para converter para cadeias de caracteres
# listas cujos elementos sejam convertiveis para
# cadeias de caracteres
def my_list2string(list):
   if list == []:
       return "[]"
   s = "[ " + str(list[0])
   for i in range(1,len(list)):
       s += ", " + str(list[i])
   return s + " ]"
    

