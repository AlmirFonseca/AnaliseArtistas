import re

import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

# Filtra o dataframe, excluindo as entradas que possuem algum dos termos na coluna indicada
def filter_dataframe(dataframe, dataframe_column, filter_terms, case_sensitive=False, reverse=False):
    
    # Gera uma lista de termos a partir do split da string recebida
    filter_terms_list = filter_terms.split(",")
    
    # Realiza um .strip() em cada termo, a fim de excluir espaços em branco desnecessários
    for term_index, term in enumerate(filter_terms_list):
        filter_terms_list[term_index] = term.strip()
    
    # Gera uma máscara "virgem", repleta de "False"
    mask = np.zeros(dataframe.shape[0], dtype=bool)
    
    # Itera sobre os termos, acumulando as máscaras geradas
    for term in filter_terms_list:
        mask = mask | dataframe[dataframe_column].str.contains(term, case=case_sensitive)
        
    # Caso o usuário deseje, a máscara é invertida
    if reverse:
        mask = ~mask
    
    # A função retorna o dataframe com a máscara aplicada
    return dataframe[~mask]

# Normaliza o conteúdo de um dataframe, a fim de facilitar a assimilação de valores de texto
def normalize_content(dataframe):
    
    # Converte todas as letras para uppercase
    dataframe = dataframe.str.upper()
    # Utiliza uma função do RegEx para excluir todos os caracteres, exceto letras e números
    dataframe = dataframe.str.replace("[^A-Za-z0-9]+", "", regex=True)
    
    # Caso haja alguma célula vazia, seu conteúdo será alterado para np.nan, o que permite que .dropna() funcione corretamente
    dataframe.replace("", np.nan, inplace=True)
    
    # A função retorna o dataframe após das alterações
    return dataframe

# Retorna uma pontuação (0 a 300) sobre a similaridade entre 2 strings
def get_simlilarity(A, B):
    
    # Converte as strings para lowercase, para aproximar os resultados
    A = A.lower()
    B = B.lower()
    
    # Remove qualquer caractere não alfanumérico utilizando RegEx
    A = re.sub("[^A-Za-z0-9]+", "", A)
    B = re.sub("[^A-Za-z0-9]+", "", B)
    
    # Caso alguma das strings sejam vazias (não existem caracteres válido após a normalização)
    if A == "" or B == "":
        similarity = -1
    # Caso as duas strings sejam idênticas, a pontuação é máxima (300)
    elif A == B:
        similarity = 300
    # Caso uma string esteja contida na outra, a pontuação é de 200
    elif (A in B) or (B in A):
        similarity = 200
    # Caso não apresentem nenhuma relação de igualdade ou contingência
    else:
        # A pontuação corresponde à Distância de Levenshtein entre as duas palavras, de 0 (pouco parecidas) a 100 (muito parecidas)
        similarity = fuzz.ratio(A, B)
    
    # A função retorna a pontuação de similaridade entre as duas strings
    return similarity

# Gera uma tabela relacional entre as músicas de um mesmo álbum em duas bases de dados diferentes
def match_tracks(df_A, df_B, similarity_threshold=0):
    # Um mesmo álbum pode conter um número diferente de faixas em diferentes plataformas
    # Nesses casos, é importante tratar como referência o álbum que possui o menor número de faixas, para evitar assimilações incorretas
    
    # Garante que df_A vai ser o album com o menor número de faixas
    if len(df_A) <= len(df_B):
        track_names_A = df_A
        track_names_B = df_B
    # Caso len(df_A) > len(df_B), a função utilizará as bases de dados na ordem inversa
    else:
        track_names_A = df_B
        track_names_B = df_A
    
    # Inicia um dataframe vazio para armazenar a relação entre o nome das faixas dos dois álbuns
    match_dataframe = pd.DataFrame(columns=["track_A", "track_B"])
    
    # Itera sobre as faixas do álbum A
    for track_name_A in track_names_A:
        
        # Inicia um dataframe vazio que armazena a pontuação de cada assimilação
        match_track = pd.DataFrame(columns=["name_A", "name_B", "pontuation"])
        
        # Compara uma faixa do álbum A com cada faixa do álbum B
        for track_name_B in track_names_B:            
            # Preenche o dataframe de assimilações com o nome da faixa no álbum A, o nome da faixa no álbum B e a pontuação de semelhança entre os nomes
            match_track.loc[len(match_track)] = [track_name_A, track_name_B, get_simlilarity(track_name_A, track_name_B)]
        
        # Após comparar uma faixa do álbum A com cada faixa do álbum B, reconhece como o melhor match o resultado com a maior pontuação
        best_track_match = match_track.sort_values(by="pontuation", ascending=False).iloc[0]
            
        if best_track_match["pontuation"] > similarity_threshold:
            # Preenche o dataframe de relações entre os nomes da faixas do álbum A com os nomes das faixas do álbum B
            match_dataframe.loc[len(match_dataframe)] = [best_track_match["name_A"], best_track_match["name_B"]]
        
    # Inicia um dataframe vazio para receber e reorganizar os dados
    result = pd.DataFrame(columns=["A", "B"])
    
    # Preenche o dataframe de resultados considerando qual das duas entradas é a maior, de modo que a coluna "A" corresponda aos nomes da faixa no álbum A, e "B" corresponda aos nomes da faixa no álbum B
    if len(df_A) <= len(df_B):
        result["A"] = match_dataframe["track_A"]
        result["B"] = match_dataframe["track_B"]
    else:
        result["A"] = match_dataframe["track_B"]
        result["B"] = match_dataframe["track_A"]

    # Retorna um dataframe que relaciona os nomes das faixas no álbum A e o nome da mesma faixa no álbum B
    return result

def match_datasets(dataset_A, dataset_B):
    
    # Obtém uma lista dos álbums em comum entre os dois álbums, a partir da coluna de nomes normalizados
    commom_albums = set(dataset_A["Normalized Album Name"]) & set(dataset_B["Normalized Album Name"])
    
    # Inicia um dataframe vazio, que irá armazenar a lista de relações entre os nomes das faixas do dataframe A e no dataframe B
    relation_AB = pd.DataFrame([])
    
    # Itera sobre cada álbum em comum
    for album_name in commom_albums:
        # Para cada álbum em comum, obtém uma lista das  de cada álbum em cada dataframe
        track_names_A = dataset_A[dataset_A["Normalized Album Name"] == album_name]["Track Name"]
        track_names_B = dataset_B[dataset_B["Normalized Album Name"] == album_name]["Track Name"]
        
        # Cria um dataframe de relações entre os nomes das músicas de um mesmo álbum
        match_track_names = match_tracks(track_names_A, track_names_B)
        # Incrementa o dataframe criado com o nome normalizado do álbum
        match_track_names["Album"] = album_name
        
        # Concatena o dataframe resultante de cada álbum num único dataframe
        relation_AB = pd.concat([relation_AB, match_track_names])
    
    # A função retorna um dataframe contendo todas as relações entre as músicas de 2 dataframes
    return relation_AB

# DEEZER ##############################################################################
# Lê o dataframe dos dados da Deezer a partir do .csv
df_deezer = pd.read_csv("discografia.csv", encoding="utf-8-sig", sep=";")

# Filtra os álbuns através da busca por termos específicos em seus títulos
df_deezer = filter_dataframe(df_deezer, "Album Name", "live,remix,edition,deluxe,radio,session,version")

# Normaliza os nomes dos álbuns a fim de permitir uma assimilação direta
df_deezer["Normalized Album Name"] = normalize_content(df_deezer["Album Name"])
# Caso não sobre nenhum caractere válido no nome do álbum após a normalização, esse álbum é descartado
df_deezer.dropna(subset=["Normalized Album Name"], inplace=True)

# Salva o dataframe já filtrado num arquivo .csv
df_deezer.to_csv("deezer_filtered.csv", encoding="utf-8-sig", sep=";", index=False)

# SPOTIFY ##############################################################################
# Lê o dataframe dos dados do spotify a partir do .csv
df_spotify = pd.read_csv("Dados das faixas - Coldplay.csv", encoding="utf-8-sig", sep=";")

# Filtra os álbuns através da busca por termos específicos em seus títulos
df_spotify = filter_dataframe(df_spotify, "Album Name", "live,remix,edition,deluxe,radio,session,version")

# Normaliza os nomes dos álbuns a fim de permitir uma assimilação direta
df_spotify["Normalized Album Name"] = normalize_content(df_spotify["Album Name"])
# Caso não sobre nenhum caractere válido no nome do álbum após a normalização, esse álbum é descartado
df_spotify.dropna(subset=["Normalized Album Name"], inplace=True)

# Salva o dataframe já filtrado num arquivo .csv
df_spotify.to_csv("spotify_filtered.csv", encoding="utf-8-sig", sep=";", index=False)

# GENIUS ##############################################################################
# Lê o dataframe dos dados da Genius a partir do .csv
df_genius = pd.read_csv("Letras - Coldplay.csv", encoding="utf-8-sig", sep=";")

# Filtra os álbuns através da busca por termos específicos em seus títulos
df_genius = filter_dataframe(df_genius, "Album Name", "live,remix,edition,deluxe,radio,session,version")

# Normaliza os nomes dos álbuns a fim de permitir uma assimilação direta
df_genius["Normalized Album Name"] = normalize_content(df_genius["Album Name"])
# Caso não sobre nenhum caractere válido no nome do álbum após a normalização, esse álbum é descartado
df_genius.dropna(subset=["Normalized Album Name"], inplace=True)

# Salva o dataframe já filtrado num arquivo .csv
df_genius.to_csv("genius_filtered.csv", encoding="utf-8-sig", sep=";", index=False)

######################################################################################

# Realiza o match entre os datasets obtidos a partir das plataformas Spotify e Genius
match_spotify_genius = match_datasets(df_spotify, df_genius)

# Reseta os indexes do dataframe, para facilitar a localização por index (.iloc[])
match_spotify_genius.reset_index(drop=True, inplace=True)
df_spotify.reset_index(drop=True, inplace=True)
df_genius.reset_index(drop=True, inplace=True)

# Cria duas novas colunas no dataframe do spotify, a fim de incorporar novas informações vindas da API da Genius
df_spotify.insert(len(df_spotify.columns), "Track Instrumental", np.nan)
df_spotify.insert(len(df_spotify.columns), "Track Lyrics", np.nan)

# Itera sobre cada match entre faixas presente no dataframe resultante do match
for i in range(len(match_spotify_genius)):
    # Para cada plataforma, obter o nome da faixa a partir da tabela relacional gerada
    spotify_track = match_spotify_genius["A"].iloc[i]
    genius_track = match_spotify_genius["B"].iloc[i]
    
    # Para cada plataforma, descobrimos o index da linha que tem os dados acerca daquela faixa
    spotify_index = df_spotify[df_spotify["Track Name"] == spotify_track].index[0]
    genius_index = df_genius[df_genius["Track Name"] == genius_track].index[0]
    
    # Com o auxílio do .iloc(), obtemos os dados que desejamos a partir da API da Genius
    track_instrumental = df_genius.iloc[genius_index]["Track Instrumental"]
    track_lyrics = df_genius[df_genius["Track Name"] == genius_track]["Track Lyrics"].values[0]
    
    # Extraímos a localização das colunas de df_spotify nas quais queremos inserir novos valores
    track_instrumental_column = df_spotify.columns.get_loc("Track Instrumental")
    track_lyrics_column = df_spotify.columns.get_loc("Track Lyrics")
    
    # Novamente, com o auxílio do .loc(), inserimos os dados obtidos no dataframe do Spotfify
    df_spotify.iloc[spotify_index, track_instrumental_column] = track_instrumental
    df_spotify.iloc[spotify_index, track_lyrics_column] = track_lyrics

# Para excluirmos as faixas que não estão presentes em ambas as bases de dados, basta dropar as linhas de "Track Instrumental" com células vazias
df_spotify.dropna(subset=["Track Instrumental"], inplace=True)
    
# Salvamos o dataframe df_spotify, agora com a letra das músicas e com o dado da faixa ser ou não ser instrumental
df_spotify.to_csv("spotify_with_lyrics.csv", encoding="utf-8-sig", sep=";", index=False)

# TODO Match no album e na musica