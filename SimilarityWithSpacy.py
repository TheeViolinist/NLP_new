import json
import spacy

from gensim import corpora, models, similarities
#adicionando comentario

resumo_nome = "SimilaridadesDicionario/similarity18.json"
#resumo_ler = input("Digite o nome dos dados .json para leitura: ")
resumo_ler = "Resumos/resumo18.json"

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






texts_dados: list()
# Leitura dos arquivos json, isso é uma lista de dicionários
with open(resumo_ler) as file:
    texts = json.load(file)
    # Lista de texto que vamos analisar a similaridade
    texts_data:list = []
    # Text irá assumir os valores de cada dicionário, então para acessar devemos utilizar somente a keyword
    # E armazenar em uma lista contendo somente os textos
    for text in texts:
        texts_data.append(text["texto"])

    texts_dados = texts




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
# Exemplo : 'Leandro' = 0, 'Ajuda' = 1...
my_dictionary = corpora.Dictionary(texts_data_treated)


len_feature = len(my_dictionary.token2id)
# Precisamos agora criar o Corpus em função do dicionário
# O Corpus é basicamente um banco de dados que vamos utilizar para treinar o modelo

# Corpus é uma lista que contém os dados de cada palavra, basicamente é uma lista que contém a importancia de cada palavra no texto
#(feature_id, feature_valuer), o id da palavra e seu valor no texto
corpus : list = []
for text in texts_data_treated:
    
    # A função do2bow transforma os dados de text em um Sparse vector, onde teremos (id, valor da palavra)
    corpus.append(my_dictionary.doc2bow(text))


# Agora, é necessário treinar o modelo, pelo modelo TF-IDF
# O modelo utiliza vários algoritmos para designar o quão importante uma palavra é para o texto
tfidf = models.TfidfModel(corpus)

# Armazena os dados para realizar a similaridade 
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = len_feature)

# realizando a similaridade com os proprios dados
similarity_data = index[tfidf[corpus]]

#Deve-se dar tolist() pois json n reconhece o tipo retornado pela tfidf
similarity_data_new = similarity_data.tolist()

#print(similarity_data_new)

dados_comparacoes = dict()
comparacoes = list()


for i in range(len(similarity_data)):
    for j in range(len(similarity_data_new[i])):
        dados_comparacoes["autor 1"] = texts_dados[i]["autor"]
        dados_comparacoes["autor 2"] = texts_dados[j]["autor"]
        dados_comparacoes["valor"] = similarity_data_new[i][j]
        comparacoes.append(dados_comparacoes.copy())
       

#Salvando os dados em .json
with open(resumo_nome, 'w') as resumo_js:
    json.dump(comparacoes, resumo_js, indent = 4, ensure_ascii=False)

resumo_js.close()

