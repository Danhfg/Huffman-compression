
# coding: utf-8

# # Importações


import sys
from tree import Tree
from node import Node
import copy     # biblioteca para copiar uma variável para outra
import binascii # biblioteca para trabalhar com binarios em ascII


# # Funções auxiliares

# ## Função que cria a árvore de Huffman


def decode(string_cod):
    if(string_cod != ""):

        stack = []

        node = Node(None, None, 'raiz', 0)
        #new_node = (None, None, 'raiz', 'raiz')
        stack.append(node)
        tree = Tree(node)

        index = 1
        while (len(stack) != 0 and index < len(string_cod)): 
            if (string_cod[index] == '0'):
                node = Node(None, None, 'n-folha', 0)
            elif(string_cod[index] == '1'):
                aux = string_cod[index + 1: index + 8];
                if(aux == '1111111'):
                    #print(aux, 'EOF')
                    node = Node(None, None, 'folha', 'EOF')
                    index+= 7
                else:
                    convert = int(aux, 2)
                    #print(aux, convert, end=' ')
                    convert = convert.to_bytes((convert.bit_length() + 7) // 8, 'big').decode()
                    #print(convert)
                    node = Node(None, None, 'folha', convert)
                    index+= 7
            if(stack[-1].get_e() == None):
                stack[-1].set_e(node)
            else:
                stack[-1].set_d(node)
                stack.pop()
            if(type(node.get_char()) == int):
                stack.append(node)
            index+=1
    return (tree.get_root(), index)


# ## Função que decodifica o resto dos caracteres lidos com base na árvore criada


def decode_char(root, pos, string):
    if(root != None):
        if(root.get_e() == None and root.get_d() == None):
            return str(root.get_char())
        pos[0] = pos[0] + 1
        if (string[pos[0]] == '0' ):
            return decode_char(root.get_e(), pos, string)
        else:
            return decode_char(root.get_d(), pos, string)


# ## Função que salva o arquivo descompactado


def salvar_arquivo_descompactado(arquivo):    
    with open('descompact.txt', 'w')as f:
        f.write(arquivo)


# # Função Principal


def main():
    cadeia_binaria = ""
    ## Leitura do arquivo binário
    #arq = 'compact.bin'
    try:
        # print command line arguments
        for arg in sys.argv[1:]:
            with open(arg, 'rb')as f:
                byte = (f.read(1))
                while len (byte)>0:# != b'':
                    #print(byte)
                    #print('{:0>8}'.format(bin(int.from_bytes(byte, byteorder=sys.byteorder))[2:]), end="")
                    cadeia_binaria +=('{:0>8}'.format(bin(int.from_bytes(byte, byteorder=sys.byteorder))[2:]) )
                    byte = f.read(1)
        

        ## Decodificação do cabeçalho e obtenção do index de onde começa o texto
        root_dec, pos = decode(cadeia_binaria)

        ## Decodificação do texto com base no cabeçalho 
        tree_dec = Tree(root_dec)
        char_atual = ""
        texto_completo = ""
        root_dec = copy.copy(tree_dec.get_root())
        pos = [pos - 1]
        while (char_atual!= "EOF"):
            root_dec = copy.copy(tree_dec.get_root())
            char_atual = decode_char(root_dec, pos, cadeia_binaria)
            texto_completo += char_atual

        ## Retirada do EOF(End Of File) do texto
        texto_completo = texto_completo[:-3]

        ## salvamento do texto completo em um arquivo 
        salvar_arquivo_descompactado(texto_completo)
        print("Arquivo descompactado com sucesso(descompact.txt)!!!!")
    except:
        print ("Não existe arquivo chamado:", arq)
        
if __name__ == "__main__":
    main()

