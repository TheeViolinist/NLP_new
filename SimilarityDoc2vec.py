import json
import spacy

import numpy as np
import gensim
import nltk
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize



resumo_nome = "../similaridadeOrientadores/similarityOrientadores14AliDoc2Vec.json"
#resumo_ler = input("Digite o nome dos dados .json para leitura: ")
resumo_ler = "../resumoOrientadores/resumoOrientadores14Alin.json"

#Acessa o token e cria uma string somente com palavras lemmatizadas
def lemmatizer_word(doc):
    text_string : str = ''

    for token in doc:    
        if token.lemma_ not in text_string:
            text_string += token.lemma_ + " "
    

    return text_string




# Vamos fazer o tratamento de texto, e remover stop words e pontuações
def remove_stop_words(docs_list : list):
    
    # Temos aqui uma matriz, onde cada elemento conterá uma lista do texto cortado e tratado
    texts_treated : list = []

    for doc in docs_list: 
        #String temporaria para armazenar o texto
        text_string : str = ''
        # Acessamos cada token do documento
        for token in doc:
            # Verifica-se se não é uma stop_word ou pontuação
            if not token.is_stop and token.pos_ != "PUNCT":
                # adiciona a string temporaria
                text_string += token.text + ' '
        
        # Armazena a string apenas sem stop_words
        texts_treated.append(text_string.lower())
    

    return texts_treated





def open_orientadores_resumo(resum_ler):
    texts_data = list()
    # Leitura dos arquivos json, isso é uma lista de dicionários
    with open(resumo_ler) as file:
        texts = json.load(file)
        # Lista de texto que vamos analisar a similaridade
        # Text irá assumir os valores de cada dicionário, então para acessar devemos utilizar somente a keyword
        # E armazenar em uma lista contendo somente os textos
        
        for text in texts:
            texts_data.append(text["texto:"])
           
            
    file.close()

    return texts_data


    
    

def main():
    nlp = spacy.load("pt_core_news_lg") # Vamos carregar os pacotes 
    nltk.download('punkt')

    # lista de documentos docs da biblioteca Spacy
    docs_list :list = []
    texts_data = open_orientadores_resumo(resumo_ler)
    
    # Primeiramente, para utilizar o gensim devemos fazer um corte nos textos e para isso vamos utilizar o framework spacy
    for text in texts_data:

        # Transforma o texto em doc, para que possamos utilziar as caracteristicas de token
        doc = nlp(text)

        # Envia o doc como parâmetro para lemmatizer_word, onde ela retorna uma string lematizada
        text_lemmatizer : str = lemmatizer_word(doc)

        # Depois adicionamos em doc_list o texto ja lematizado
        docs_list.append(nlp(text_lemmatizer))


    


    # Remove-se a stop words
    # texts_data_treated representa os textos sem stop words e palavras lemmatizadas
    #texts_data_treated : list = remove_stop_words(docs_list)
    texts_data_treated = texts_data
    
    # Agora vamos treinar o modelo, primeiramente vamos idenficar nossos dados
    # Enumerate() pega tanto o indice como valor da lista
    # Basicamente estamos indicando os dados do nosso documento em forma de token para facilitar o treinamento, onde vamos ter uma lista que contém as palavras 
    # do texto tokenizada e indicada por uma determinada tag
    tagged_data = [TaggedDocument(words=word_tokenize(text, language='portuguese'), tags=[str(i)]) for i, text in enumerate(texts_data_treated)]
    
    
    # Podemos realizar o treinamento do modelo, epochs significa a quantia de vezes que será feito o algoritmo para treinamento
    model = gensim.models.doc2vec.Doc2Vec(epochs=100)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=100)
    model.save("similarity.model")

    model = Doc2Vec.load("similarity.model")
    
    matrix_length = len(texts_data_treated)
    similarity_matrix = np.zeros((matrix_length, matrix_length))
    

    similarity_data = list()  
    

    for i in range(matrix_length):
        data = dict()
        data["indice"] = i
        similarity_string = ''
        for j in range(matrix_length):
            similarity_matrix[i, j] = model.dv.similarity(i, j)
            similarity_string += str(round(similarity_matrix[i][j], 2)) + ' '
        
        data['similaridade'] = similarity_string

        similarity_data.append(data)
    
    

    with open(resumo_nome, 'w') as similaridade_js:
        json.dump(similarity_data, similaridade_js, indent=4)
   


if __name__== '__main__':
    main()