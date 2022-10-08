import re
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

# Filtra o dataframe, excluindo as entradas que possuem algum dos termos na coluna indicada
def filter_dataframe(dataframe, dataframe_column, filter_terms="", case_sensitive=False, reverse=False):
    """
    Filtra o dataframe a partir dos termos indicados na coluna indicada

    :param dataframe: Dataframe a ser filtrado
    :type dataframe: `pandas.core.frame.DataFrame`
    :param dataframe_column: Coluna do Dataframe indicado a ser analisada
    :type dataframe_column: `str`
    :param filter_terms: Termos a serem utilizados como filtro, padrão como ``""``
    :type filter_terms: `str`, opcional
    :param case_sensitive: Opção de filtro utilizando "case sensitive", padrão como ``False``
    :type case_sensitive: `bool`, opcional
    :param reverse: Opção de filtro invertido, padrão como ``False``
    :type reverse: `bool`, opcional
    :return: Dataframe filtrado
    :rtype: `pandas.core.frame.DataFrame`
    """
    # Caso não haja termos a serem filtrados, a função retorna o próprio dataframe
    if not filter_terms:
        return dataframe
    
    # Gera uma lista de termos a partir do split da string recebida
    filter_terms_list = filter_terms.split(",")
    
    # Realiza um .strip() em cada termo, a fim de excluir espaços em branco desnecessários
    for term_index, term in enumerate(filter_terms_list):
        filter_terms_list[term_index] = term.strip()
        
    # Caso não haja termos a serem filtrados, a função retorna o próprio dataframe
    if len(filter_terms_list) == 0:
        return dataframe
    
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
    """
    Normaliza o conteúdo de um dataframe para facilitar a assimilação de valores de texto

    :param dataframe: Dataframe a ser normalizado
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Dataframe normalizado
    :rtype: `pandas.core.frame.DataFrame`
    """
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
    """
    Algoritmo de pontuação de simililaridade entre duas strings, para compreender o quão próximas estão uma da outra

    :param A: Primeira string a ser analisada
    :type A: `str`
    :param B: Segunda string a ser analisada
    :type B: `str`
    :return: Pontuação de simililaridade
    :rtype: `int`
    """
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
    """
    Função que gera um dataframe com a relação entre as mesmas músicas de um mesmo álbum, 
    mas em bases de dados diferentes, afim de procurar músicas existentes em uma base de dados, 
    mas não em outra, além de simililaridades entre si

    :param df_A: Primeiro Dataframe contendo as músicas de um determinado álbum
    :type df_A: `pandas.core.frame.DataFrame`
    :param df_B: Segundo Dataframe contendo as músicas do mesmo álbum
    :type df_B: `pandas.core.frame.DataFrame`
    :param similarity_threshold: Grau de similaridade utilizando um algoritmo de similaridade, padrão como ``0``
    :type similarity_threshold: `int`, opcional
    :return: Dataframe relacional entre as mesmas músicas de um mesmo álbum, mas em bases de dados diferentes.
    :rtype: `pandas.core.frame.DataFrame`
    """
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
    """
    Função que gera um dataframe contendo todas as relações entre as músicas de dois dataframes diferentes

    :param dataset_A: Primeiro dataframe contendo todos os álbuns e músicas de uma primeira base de dados
    :type dataset_A: `pandas.core.frame.DataFrame`
    :param dataset_B: Segundo dataframe contendo todos os álbuns e músicas de uma segunda base de dados
    :type dataset_B: `pandas.core.frame.DataFrame`
    :return: Dataframe contendo todas as relações encontradas entre as músicas e álbuns de dois dataframes diferentes
    :rtype: `pandas.core.frame.DataFrame`
    """
    
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

def append_lyrics_and_instrumental(df_spotify, df_genius):
    """
    Função para adição de letras e instrumental a partir da plataforma Genius em um 
    dataframe contendo álbuns e músicas de um artista da plataforma Spotify, considerando a relação encontrada 
    entre as músicas e álbuns encontrados em cada plataforma

    :param df_spotify: Dataframe contendo os dados de músicas e álbuns de um artista na plataforma Spotify
    :type df_spotify: `pandas.core.frame.DataFrame`
    :param df_genius: Dataframe contendo os dados de letra e instumental das músicas e álbuns de um artista na plataforma GeniusLyrics
    :type df_genius: `pandas.core.frame.DataFrame`
    :return: Dataframe gerado contendo letras e instrumental das músicas e álbuns junto dos dados da plataforma Spotify
    :rtype: `pandas.core.frame.DataFrame`
    """
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
        
    # A função retorna o dataframe com os dados do Spotify, agora contendo os novos dados/colunas nele adicionados
    return df_spotify

def append_genre(df_spotify, df_deezer):
    """
    Função para adição de gênero de álbuns e músicas a partir da plataforma Deezer em um 
    dataframe contendo álbuns e músicas de um artista da plataforma Spotify, considerando a relação encontrada 
    entre as músicas e álbuns encontrados em cada plataforma

    :param df_spotify: Dataframe contendo os dados de músicas e álbuns de um artista na plataforma Spotify
    :type df_spotify: `pandas.core.frame.DataFrame`
    :param df_genius: Dataframe contendo os dados de gênero das músicas e álbuns de um artista na plataforma Deezer
    :type df_genius: `pandas.core.frame.DataFrame`
    :return: Dataframe gerado contendo gênero de músicas e álbuns junto dos dados da plataforma Spotify
    :rtype: `pandas.core.frame.DataFrame`
    """
    # Realiza o match entre os datasets obtidos a partir das plataformas Spotify e Deezer
    match_spotify_deezer = match_datasets(df_spotify, df_deezer)
    
    # Reseta os indexes do dataframe, para facilitar a localização por index (.iloc[])
    match_spotify_deezer.reset_index(drop=True, inplace=True)
    df_spotify.reset_index(drop=True, inplace=True)
    df_deezer.reset_index(drop=True, inplace=True)
    
    # Cria novas colunas no dataframe do spotify, a fim de incorporar novas informações vindas da API da Deezer
    df_spotify.insert(len(df_spotify.columns), "Genre", np.nan)
    
    # Itera sobre cada match entre faixas presente no dataframe resultante do match
    for i in range(len(match_spotify_deezer)):
        # Para cada plataforma, obter o nome da faixa a partir da tabela relacional gerada
        spotify_track = match_spotify_deezer["A"].iloc[i]
        deezer_track = match_spotify_deezer["B"].iloc[i]
        
        # Para cada plataforma, descobrimos o index da linha que tem os dados acerca daquela faixa
        spotify_index = df_spotify[df_spotify["Track Name"] == spotify_track].index[0]
        deezer_index = df_deezer[df_deezer["Track Name"] == deezer_track].index[0]
        
        # Com o auxílio do .iloc(), obtemos os dados que desejamos a partir da API da Deezer        
        track_genre = df_deezer.iloc[deezer_index]["Genre"]
        
        # Extraímos a localização das colunas de df_spotify nas quais queremos inserir novos valores
        track_genre_column = df_spotify.columns.get_loc("Genre")
        
        # Novamente, com o auxílio do .loc(), inserimos os dados obtidos no dataframe do Spotfify
        df_spotify.iloc[spotify_index, track_genre_column] = track_genre
        
    # Caso quiséssemos excluirmos as faixas que não estão presentes em ambas as bases de dados, basta dropar as linhas de "Genre" com células vazias
    # Como não queremos habilitar essa opção, essa linha permanecerá comentada
    # df_spotify.dropna(subset=["Genre"], inplace=True)
        
    # A função retorna o dataframe com os dados do Spotify, agora contendo os novos dados/colunas nele adicionados
    return df_spotify

# TODO Match no album e na musica
