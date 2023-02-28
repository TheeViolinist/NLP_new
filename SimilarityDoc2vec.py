import json
import spacy

import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec


resumo_nome = "../similaridadeOrientadores/similarityOrientadores14.txt"
#resumo_ler = input("Digite o nome dos dados .json para leitura: ")
resumo_ler = "../resumoOrientadores/resumoOrientadores14.json"

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
        
        # corta a string tratada e armazena na lista
        texts_treated.append(text_string.split())
    

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



def tagged_document(list_words):
    
    

def main():
    nlp = spacy.load("pt_core_news_lg") # Vamos carregar os pacotes 
    
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
    # Em texts_data_treated temos uma matriz quadrada, onde cada elemento contém outra lista, no qual essa lista
    # Representada o conjunto de palavras de cada texto tratado, por exemplo, o texto 1 vai conter as seguintes palavras lemmatizadas e sem stop words
    texts_data_treated : list = remove_stop_words(docs_list)

    #Agora vamos treinar o modelo, primeiramente vamos idenficar nossos dados
    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower())), tags=[str(i)] for in, _d in enumerate(data)]
   

if __name__== '__main__':
    main()