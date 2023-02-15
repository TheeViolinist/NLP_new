import json
import re

#nome_arquivo_resumo = str(input("Digite o nome do arquivo/caminho de resumo: "))
#nome_arquivo_instance = str(input("Digite o nome do arquivo de instancia a ser criado: "))
#nome_arquivo_dic = str(input("Digite o arquivo/caminho de dicionário da instancia: "))
#nome_arquivo_instancia = str(input("Digite o arquivo/caminho da instancia:"))
nome_arquivo_instancia = "../instance_campusCCHSA_dia4.txt"
nome_arquivo_dic = "../dictionary_campusCCHSA_dia4.txt"
nome_arquivo_resumo = "resumo14.json"
nome_arquivo_diconario_new = "dictionary_campusCCHSA_dia4.txt"

def abreArquivoResumo(nome_arquivo_resumo: str) :

    resumos = list()

    with open(nome_arquivo_resumo) as resumos_arquivo:
        resumos = json.load(resumos_arquivo)
    
    resumos_arquivo.close()

    return resumos


def abreArquivoDicionario(nome_arquivo_dicionario: str) :

    dic = list()

    with open(nome_arquivo_dicionario, 'r') as arquivo:

        dic = arquivo.readlines()
    
    arquivo.close()

    return dic



def abreArquivoInstancia(nome_arquivo_instancia: str) :

    instance_dados = list()

    with open(nome_arquivo_instancia, 'r') as instancia:

        instance_dados = instancia.readlines()
    
    instancia.close()
    
    return instance_dados



def retornaMatrizNomes(dicionario:list, quantia_autores: int):

    dados_autores = list()

    for i in range(quantia_autores):

        dados_autores.append(dicionario[i].split(' ', 1))


    return dados_autores


       

def menor_indice(valor):

    linha = valor.split()

    return int(linha[0])



def retorna_sem_espaco(linha:str):


    indice = 0
    novo_texto: str
    
    while(1):

        if linha[0] != ' ':
            break
        
        linha = linha.replace(linha[indice], "", 1)


    linha = linha.rstrip()
    return linha


resumos = abreArquivoResumo(nome_arquivo_resumo)
dicionario = abreArquivoDicionario(nome_arquivo_dic)
instance_dados = abreArquivoInstancia(nome_arquivo_instancia)

dados_autores_instance = instance_dados[1].split()
quantia_autores = int(dados_autores_instance[0])


dados_autores = retornaMatrizNomes(dicionario, quantia_autores)


file_dados = list()


for resumo in resumos:

    for autor in dados_autores:
        
        name_autor = autor[1].replace('\n', '')

        if resumo["autor"] == name_autor:
            file_content = autor[0] + ' ' + resumo["titulo"] + '\n'
            file_dados.append(file_content)

    
    file_content = ''



file_dados.sort(key=menor_indice)



for linha in file_dados:

    linha_dados_nova = linha.replace('\n', '')
    linha_dados = linha_dados_nova.split(' ', 1)
    indice_autor = int(linha_dados[0]) #Pega-se o indice da linha
    i = 0
    
    for linha_dicionario in dicionario:
        
        linha_nova_dicionario = linha_dicionario.replace('\n', '')
        
        linha_dicionario_dados = linha_nova_dicionario.split(' ', 1)
        

        text_new = ''
        if len(linha_dicionario_dados) > 1:
            indice_autor_dicionario = int(linha_dicionario_dados[0]) #Pega-se o indice da linha do dicionario

        if indice_autor_dicionario == indice_autor and i < quantia_autores:

            text_new = linha_nova_dicionario + '\t' + retorna_sem_espaco(linha_dados[1]) + '\n'

            dicionario[i] = text_new

        
        i += 1
        


file_write = open(nome_arquivo_diconario_new, 'w')


for linha in dicionario:

    file_write.write(linha)

    

file_write.close()









