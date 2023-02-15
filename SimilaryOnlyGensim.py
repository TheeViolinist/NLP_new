import json
import spacy

from gensim import corpora, models, similarities


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







# Leitura dos arquivos json, isso é uma lista de dicionários
with open("resumo1.json") as file:
    texts = json.load(file)




# Lista de texto que vamos analisar a similaridade
texts_data:list = []
# Text irá assumir os valores de cada dicionário, então para acessar devemos utilizar somente a keyword
# E armazenar em uma lista contendo somente os textos
for text in texts:
    texts_data.append(text["texto"])





nlp = spacy.load("pt_core_news_lg") # Vamos carregar os pacotes 

# lista de documentos docs da biblioteca Spacy
docs_list :list = []

# Primeiramente, para utilizar o gensim devemos fazer um corte nos textos e para isso vamos utilizar o framework spacy
for text in texts_data:

    # Transforma o texto em doc, para que possamos utilziar as caracteristicas de token
    doc = nlp(text)

    # Envia o doc como parâmetro para lemmatizer_word, onde ela retorna uma string lematizada
    text_lemmatizer : str = lemmatizer_word(doc)

    # Depois adicionamos em doc_list o texto ja lematizado
    docs_list.append(nlp(text_lemmatizer))




# Remove-se a stop words
# Em texts_data_treated temos uma matriz, onde cada elemento contém outra lista, no qual essa lista
# Representada o conjunto de palavras de cada texto tratado
texts_data_treated : list = remove_stop_words(docs_list)


# Cria um dicionário em relação cada palavra na lista, basicamente vamos associar cada palavra um numero
my_dictionary = corpora.Dictionary(texts_data_treated)



# Precisamos agora criar o Corpus em função do dicionário
# O Corpus é basicamente um banco de dados que vamos utilizar para treinar o modelo

# Corpus é uma lista que contém os dados de cada texto
corpus : list = []
for text in texts_data_treated:
    
    # A função do2bow transforma os dados de text em um Sparse vector, onde teremos (id, valor da palavra)
    corpus.append(my_dictionary.doc2bow(text))


print('Corpus: ', corpus)
    



    
