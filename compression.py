
# coding: utf-8

# # Importações


import sys
from tree import Tree
from node import Node
import copy     # biblioteca para copiar uma variável para outra
import binascii # biblioteca para trabalhar com binarios em ascII


# # Funções Auxiliares

# ## Função para encontrar os dois nós com menores pesos


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


# ## Função para imprimir uma árvore em pré-ordem


def pre_ordem(node, s):
    if(node != None):
        print(str(s)+str(node.get_char()))
        pre_ordem(node.get_e(), s+"|")
        pre_ordem(node.get_d(), s+"|")


# ## Função para criar a tabela de compactação em pré-ordem


def tabela_pre(node, caminho, t):
    if(node != None):
        if(type(node.get_char()) == str ):
            t[node.get_char()] = ''.join(caminho)
        else:
            caminho_e = caminho[:]
            caminho_d = caminho[:]
            caminho_e.append('0')
            caminho_d.append('1')
            tabela_pre(node.get_e(), caminho_e, t)
            tabela_pre(node.get_d(), caminho_d, t)


# ## Função para criar o cabeçalho do arquivo


def cab(node, cabecalho_final,tabela_final):
    if(node != None):
        if(type(node.get_char()) == str):
            cabecalho_final[0] += '1'
            if (node.get_char() == 'EOF'):
                cabecalho_final[0] += '1111111'
                
            else:
                cabecalho_final[0] += '{:0>7}'.format(bin(int.from_bytes(node.get_char().encode(), 'big'))[2:])
        else:
            cabecalho_final[0] += '0'
        cab(node.get_e(), cabecalho_final,tabela_final)
        cab(node.get_d(), cabecalho_final,tabela_final)


# ## Função para salvar o arquivo


def salvar_arquivo(arquivo):    
    with open('compact.bin', 'wb')as f:
        i = 0
        while (i < len(arquivo)):
            if(i + 8 > len(arquivo)):
                n = int('{:0<8}'.format(arquivo[i:]), 2)
                f.write(n.to_bytes((n.bit_length() + 7) // 8, 'big'))
                #print(n.to_bytes((n.bit_length() + 7) // 8, 'big'))
            else:
                n = int(arquivo[i:i+8], 2)
                if (n == 0):
                    f.write(b'\x00')
                    #print(b'\x00')
                else:
                    f.write(n.to_bytes((n.bit_length() + 7) // 8, 'big'))
                    #print(n.to_bytes((n.bit_length() + 7) // 8, 'big'))
            i += 8


# ## Função principal que cria o arquivo compactado


def main():
    conteudo = ""
    # print command line arguments

    try:
        for arg in sys.argv[1:]:
            print(arg)
            with open(arg, 'r') as file:
                conteudo += file.read()
        tabela_inicial = {}
        for i in list(conteudo):
            tabela_inicial[i] = list(conteudo).count(i)
        tabela_inicial["EOF"] = 1
        #print(tabela_inicial)
        
        nodes = []
        #Criar lista de árvores com um nó
        for chave in tabela_inicial:
            nodes.append(Node(None, None, tabela_inicial[chave], chave))

        #Algoritmo de Huffman
        while len(nodes) > 1:
            menores = menores_nodes (nodes)
            node_pai = Node(menores[0], menores[1],
                            menores[0].get_apar() + menores[1].get_apar(),
                            menores[0].get_apar() + menores[1].get_apar())
            nodes.remove(menores[0])
            nodes.remove(menores[1])
            nodes.append(node_pai)

        #criação da árvore
        tree = Tree(nodes[0])
        root = tree.get_root()
        #r = tree.get_root()
        #pre_ordem(r, "")
        
        #Criação da tabela de codificação
        tabela_final = {}
        tabela_pre(root, [], tabela_final)
        print("Tabela de codificação: ", tabela_final)
        
        #Codificação do texto a partir da tabela
        cod = ""
        for i in conteudo:
            cod += tabela_final[i]
        #Adicionar sinalização de final do arquivo
        cod += tabela_final['EOF']
        
        #Criando cabeçalho do arquivo
        cab_e_texto = [""]
        cab(root, cab_e_texto,tabela_final)
        cab_e_texto = cab_e_texto[0]
        #print(cab_e_texto)
        
        #Unificando cabeçalho e o conteudo do texto já em binário
        arquivo = cab_e_texto + cod
        arquivo[:]
        
        salvar_arquivo(arquivo)
        print("Arquivo compactado criado com sucesso (compact.txt)!!!!!")

    except:
        print ("Não existe arquivo chamado")

if __name__ == "__main__":
    main()

