import sys
from tree import Tree
from node import Node
import copy
import binascii

def menores_nodes(nodes):
    #m1, m2 = float('inf'), float('inf')
    m1 = Node(None, None, float('inf'),'inf')
    m2 = Node(None, None, float('inf'),'inf')
    for x in nodes:
        if x.get_apar() < m1.get_apar():
            m1, m2 = x, m1
        elif x.get_apar() < m2.get_apar():
            m2 = x
    return m1,m2

def main():
    conteudo = ""
    # print command line arguments
    for arg in sys.argv[1:]:
        print(arg)
        with open(arg, 'r') as file:
            conteudo += file.read()
    tabela_inicial = {}
    for i in list(conteudo):
        tabela_inicial[i] = list(conteudo).count(i)
    tabela_inicial["EOF"] = 1
    #print(tabela_inicial)

if __name__ == "__main__":
    main()
