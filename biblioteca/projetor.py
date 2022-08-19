import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import NMF

#Texto e palavras chaves:
#target = "solutions on waste and water, Improve water quality and water efficiency use, water contamination, water for human consumption, water resources".split(" ")

def proj(target):

    target_list = target.split(",")

    #Lendo a base o arquivo CSV:
    df = pd.read_csv('../canada_amostra.csv')
    #df.shape = (21299, 8) ------> 8 features e 21299 exemplos

    Numero_de_exemplos = df.shape[0]



    #Achando a correspondência entre tema e a melhor descrição e, consequentemente, a melhor empresa. Vamos usar o algorítmo "Próximo vizinho" (Nearest Neighbor)
    #TfidVectorize transforma as 5000 palavras mais relevantes em features binárias de 0 ou 1.
    vec = TfidfVectorizer(max_features=5000, stop_words="english", max_df=0.95, min_df=2) #min_df = mńimio de contagem p/a palavra ser contada como feature
                                                                                          #max_df = máx. de freq. p/que a palara seja contada como feature
    features = vec.fit(df.description)
    features = vec.transform(df.description)  #Uma matrix com a dimensão de (Numero_de_exemplos, 5000)

    #Fitando no modelo Nearest Neighbor (https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)
    from sklearn.neighbors import NearestNeighbors
    knn = NearestNeighbors(n_neighbors=20, metric='cosine')
    knn.fit(features)


    ### RESPOSTA DA PERGUNTA
    target = "solutions on waste and water,Improve water quality and water efficiency use,water contamination,water for human consumption,water resources"

    target_list = target.split(",")

    temas = target_list#["any recommendations for good ftp sites?", "i need to clean my car"]
    input_features = vec.transform(temas)

    # Resposta com as distâncias D e o número de vizinhos N
    D, N = knn.kneighbors(input_features, n_neighbors=20, return_distance=True)

    df_respostas = pd.DataFrame

    lista_temas = []
    nomes = []
    cidades = []
    empregados = []
    aportes = []
    lista_lat = []
    lista_lng = []

    resposta_inteira = "=" * 100

    for tema, distances, neighbors in zip(temas, D, N):
        print("Tema de busca = " + " '" + str(tema) + "'", "\n")
        resposta_inteira = resposta_inteira + "<p>" + "<b>" + "Tema de busca = " + "</b>" + " '" + "<b>" + str(tema) + "</b>" + "'" + "</p>"
        for dist, neighbor_idx in zip(distances, neighbors):
            nome_da_empresa = df.name.loc[neighbor_idx].capitalize()
            cidade_da_empresa = df.city.loc[neighbor_idx].capitalize()
            numero_de_empregados = df.employees.loc[neighbor_idx]
            aporte_da_empresa = df.total_funding.loc[neighbor_idx]
            lat = df.lat.loc[neighbor_idx]
            lng = df.lng.loc[neighbor_idx]

            lista_temas.insert(len(lista_temas), tema)
            nomes.insert(len(nomes), nome_da_empresa)
            cidades.insert(len(cidades), cidade_da_empresa)
            empregados.insert(len(empregados), numero_de_empregados)
            aportes.insert(len(aportes), aporte_da_empresa)
            lista_lat.insert(len(lista_lat), lat)
            lista_lng.insert(len(lista_lng), lng)

            nova_linha = [
                {"tema": tema, "nome": nome_da_empresa, "cidade": cidade_da_empresa, "empregados": numero_de_empregados,
                 "aporte": aporte_da_empresa}]
            # df_respostas = df_respostas.append(nova_linha, ignore_index=True)

            parte_1 = "<p>" + "Distância KNN = " + str(round(dist, 3)) + ". Neighbor idx = " + str(neighbor_idx) + "</p>"
            parte_2 = "<p>" + "Nome da empresa: " + nome_da_empresa + ". Cidade: " + cidade_da_empresa + "</p>"

            print(parte_1)
            print(parte_2)

            resposta_inteira = resposta_inteira + parte_1 + parte_2

            print("-" * 70)
        resposta_inteira = resposta_inteira + "<p>" + "=" * 100 + "</p>"
        print("=" * 100)
        print()

    #Cria um dataframe de todas as respostas
    data = {"tema":lista_temas, "nome":nomes, "cidade":cidades, "empregados":empregados, "aporte":aportes, "X": lista_lng, "Y": lista_lat}
    df_respostas = pd.DataFrame(data)


    return resposta_inteira

