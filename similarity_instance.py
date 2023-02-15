import json


nome_similaridade_arquivo = "SimilaridadesDicionario/similarity18.json"
nome_instance = "dadosCse/Enic18/instance_campusCCTA_dia18.txt"
nome_instance_dic = "dadosCse/Enic18/dictionary_campusCCTA_dia18.txt"
nome_instance_similarity = "InstanceSimilarityCse/instance_similarity_campusCCTA_dia18.txt"

similarity_data = str()
similarity_data_list = list()
quantia_autores = 0


def abre_similaridade():
    similarities = list()
    with open(nome_similaridade_arquivo) as file:
        similarities = json.load(file)

    file.close()
    return similarities


def abre_instancia():

    instance = list()
    with open(nome_instance, 'r') as instances:
        instance = instances.readlines()


    instances.close()
    return instance


def abre_dicionario():

    instance_dic_lines = list()
    with open(nome_instance_dic, 'r') as dic:
        instance_dic_lines = dic.readlines()

    dic.close()
    return instance_dic_lines



def retorna_posicao_author_similaridade(similarities: list, name: str):
    posicao = 0

    for similarity in similarities:

        if name == similarity["autor 1"]:
            return posicao

        posicao += 1

    return -1


def retorna_posicao_lista_autores(authors: list, name: str):
    posicao = 0

    for author in authors:
        name_author = author[1].replace('\n', '')

        if name_author == name:
            return posicao
        posicao += 1

    return -1


similarities = abre_similaridade()
instance = abre_instancia()
instance_dic_lines = abre_dicionario()



file_write = open(nome_instance_similarity, 'w')
file_content = str()


dados_autores = instance[1].split()  # Retorna os dados dos autores
quantia_autores = int(dados_autores[0]) # recebe a quantia de autores



for i in range(quantia_autores):
    # Similarity_data_list é uma matriz, na qual contém no indice 0 o numero de determinado autor e depois seu nome
    # Utiliza isso para quebrar no primeiro espaço
    similarity_data_list.append(instance_dic_lines[i].split(' ', 1))

# Para cada autor
for author in similarity_data_list:

    name_author = author[1].replace('\n', '') # retira o \n do nome para poder fazer a igualdade
    # Pega a sua posição em similaridade
    posicao_author_1 = retorna_posicao_author_similaridade(similarities, name_author)
    # Verifica se ele foi achado
    if posicao_author_1 != -1:
        file_content = author[0] # inicia a string
    
        while 1:
            if name_author != similarities[posicao_author_1]["autor 1"] or posicao_author_1 >= len(similarities) - 1:
                break
            posicao_author_2 = retorna_posicao_lista_autores(similarity_data_list, similarities[posicao_author_1]["autor 2"]) # Pega a posiçao do autor 2 na lista
        
            # Caso achado
            if posicao_author_2 != -1:
                similarity_value = 0
                file_content += similarity_data_list[posicao_author_2][0] + ' ' + "{similarity_value:.2f}" + '\n'
                file_content = file_content.format(similarity_value = similarities[posicao_author_1]["valor"])
                file_write.write(file_content)
                

            posicao_author_1 += 1
            file_content = author[0] + ' '

file_write.close()
