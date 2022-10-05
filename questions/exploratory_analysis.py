''' Módulo de Análise exploratória 

Esse módulo contém funções responsáveis por responder perguntas a partir da análise de dataframes em um formato específico.
O formato do dataframe deve ser igual ao gerado pelo módulo database nesse mesmo repositório e lido pela função create_dataframe.

'''

#Importe as bibliotecas necessárias
import pandas as pd
import numpy as np
import collections


# Recebe um dataframe e retorna as 3 músicas mais ouvidas por álbum
def most_listened_by_album(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas mais ouvidas por álbum

    :param dataframe: DataFrame com 'Album Name' como parte do multi index e com coluna 'Popularity'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas mais ouvidas por álbum, caso haja mais músicas com a mesma popularidade, todas serão retornadas.
    :rtype: pandas.core.frame.DataFrame

    """
    grouped = dataframe.groupby('Album Name')['Popularity'].nlargest(3,keep='all') # Agrupa por 'Album Name' e seleciona os 3 maiores valores da coluna 'Popularity'
    grouped = grouped.reset_index(level = 0) 
    grouped.drop(columns='Album Name',inplace = True)
    return grouped

# Recebe um dataframe e retorna as 3 músicas menos ouvidas por álbum  
def least_listened_by_album(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas menos ouvidas por álbum

    :param dataframe: DataFrame com 'Album Name' como parte do multi index e com coluna 'Popularity'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas menos ouvidas por álbum, caso haja mais músicas com a mesma popularidade, todas serão retornadas.
    :rtype: pandas.core.frame.DataFrame

    """
    grouped = dataframe.groupby('Album Name')['Popularity'].nsmallest(3,keep='all') # Agrupa por 'Album Name' e seleciona os 3 menores valores da coluna 'Popularity'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album Name',inplace = True)
    return grouped
    
# Recebe um dataframe e retorna as 3 músicas mais longas por álbum  
def longest_by_album(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas mais longas por álbum

    :param dataframe: DataFrame com 'Album Name' como parte do multi index e com coluna 'Duration'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas mais longas por álbum, caso haja mais músicas com a mesma duração, todas serão retornadas.
    :rtype: pandas.core.frame.DataFrame

    """
    grouped = dataframe.groupby('Album Name')['Duration'].nlargest(3,keep='all') # Agrupa por 'Album Name' e seleciona os 3 maiores valores da coluna 'Duration'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album Name',inplace = True)
    return grouped
    
# Recebe um dataframe e retorna as 3 músicas menos longas por álbum
def shortest_by_album(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas mais curtas por álbum

    :param dataframe: DataFrame com 'Album Name' como parte do multi index e com coluna 'Duration'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas mais curtas por álbum, caso haja mais músicas com a mesma popularidade, todas serão retornadas.
    :rtype: pandas.core.frame.DataFrame

    """ 
    grouped = dataframe.groupby('Album Name')['Duration'].nsmallest(3,keep='all') # Agrupa por 'Album Name' e seleciona os 3 menores valores da coluna 'Duration'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album Name',inplace = True)
    return grouped

# Recebe um dataframe e retorna as 3 músicas mais ouvidas na história do artista
def most_listened(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas mais ouvidas 

    :param dataframe: DataFrame com coluna 'Popularity'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas mais ouvidas, caso haja mais músicas com a mesma popularidade, todas serão retornadas.
    :rtype: pandas.core.frame.DataFrame

    """ 
    return dataframe.nlargest(3, 'Popularity',keep='all')

# Recebe um dataframe e retorna as 3 músicas menos ouvidas na história do artista
def least_listened(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas menos ouvidas 

    :param dataframe: DataFrame com coluna 'Popularity'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas menos ouvidas, caso haja mais músicas com a mesma popularidade, todas serão retornadas..
    :rtype: pandas.core.frame.DataFrame

    """ 
    return dataframe.nsmallest(3, 'Popularity',keep='all')

# Recebe um dataframe e retorna as 3 músicas mais longas na história do artista
def longest(dataframe):
    """Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas mais longas

    :param dataframe: DataFrame com coluna 'Duration'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com 3 músicas mais longas, caso haja mais músicas com a mesma duração, todas serão retornadas.
    :rtype: pandas.core.frame.DataFrame

    """ 
    return dataframe.nlargest(3, 'Duration',keep='all')
    
# Recebe um dataframe e retorna as 3 músicas menos longas na história do artista
def shortest(dataframe):
    """Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas mais curtas

    :param dataframe: DataFrame com coluna 'Duration'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com 3 músicas mais curtas, caso haja mais músicas com a mesma duração, todas serão retornadas.
    :rtype: pandas.core.frame.DataFrame

    """ 
    return dataframe.nsmallest(3, 'Duration',keep='all')

# Recebe uma lista com algumas strings contendo itens separados por '/' e retorna um array com valores únicos dos itens
def unique_values(array):
    """Recebe uma lista com algumas strings contendo itens separados por '/' e retorna um array com valores únicos dos itens

    :param array: Lista com alguns itens sendo palavras separadas por '/'.
    :type array: list
    :return: Array com todas as palavras contidas no array de input, incluindo as separadas por '/'. Toda palavra só aparecerá uma única vez.
    :rtype: np.ndarray

    """
    
    unique_values_array = []
    for i in range(len(array)):
        array_item = array[i].split("/")
        for item in array_item:
            unique_values_array.append(item)
    unique_values_array = np.asarray(unique_values_array)
    unique_values_array = np.unique(unique_values_array)
    return unique_values_array

# Recebe uma dataframe e retorna os 3 álbuns com mais prêmios
def albuns_awards(dataframe):
    """Recebe um dataframe no formato pandas e retorna um dataframe com as 3 álbuns mais premiados e suas quantidades de prêmios

    :param dataframe: DataFrame com multi index e com coluna 'Awards'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com os álbuns mais premiados e a quantidade de prêmios recebidos.
    :rtype: pandas.core.frame.DataFrame

    """
    grouped = dataframe.groupby(level=0)
    dictionary_quantity_awards = {}
    for album, album_dataframe in grouped:
        awards = album_dataframe["Awards"].values
        dictionary_quantity_awards[album]=len(unique_values(awards))
    quantity_awards_dataframe = pd.DataFrame(dictionary_quantity_awards.values(),dictionary_quantity_awards.keys(),columns=["Awards"])
    most_recognized = quantity_awards_dataframe.nlargest(3,'Awards')
    return most_recognized

# Recebe um dataframe e retorna a correlação de Pearson entre duração e popularidade das músicas
def duration_popularity(dataframe):
    """Recebe um dataframe no formato pandas e retorna um float com a correlação de pearson entre duração e popularidade.

    :param dataframe: Dataframe com as colunas Duration e Popularity.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Correlação de pearson entre as colunas Duration e Popularity.
    :rtype: numpy.float64

    """
    correlation = dataframe.corr(method ='pearson')
    return correlation.loc["Duration","Popularity"]

# Recebe um dataframe e retorna as 10 palavras mais comuns nos títulos dos álbuns
def common_words_by_album(dataframe):
    """Recebe um dataframe e retorna as 10 palavras mais comuns nos títulos dos álbuns.

    :param dataframe: Dataframe com multi index.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Lista com tuplas contendo as palavras mais comuns nos títulos dos álbuns e suas frequências.
    :rtype: list

    """
    albuns = dataframe.index.get_level_values(0)
    albuns_list = list(dict.fromkeys(albuns))
    words_list = []
    for album in albuns_list:
        words = album.split()
        for word in words:
            words_list.append(word) 
    counter = collections.Counter(words_list)
    most_commom = counter.most_common(10)
    return most_commom
    
# Recebe um dataframe e retorna as 10 palavras mais comuns nos títulos das músicas
def common_words_by_song(dataframe):
    """Recebe um dataframe e retorna as 10 palavras mais comuns nos títulos das músicas

    :param dataframe: Dataframe com multi index.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Lista com tuplas contendo as palavras mais comuns nos títulos das músicas e suas frequências.
    :rtype: list

    """
    songs = dataframe.index.get_level_values(1)
    songs_list = list(dict.fromkeys( songs))
    words_list = []
    for song in songs_list:
        words = song.split()
        for word in words:
            words_list.append(word) 
    counter = collections.Counter(words_list)
    most_commom = counter.most_common(10)
    return most_commom
    
# Recebe um dataframe e retorna as 10 palavras mais comuns nas letras das músicas
def common_words_by_lyrics(dataframe):
    """Recebe um dataframe e retorna as 10 palavras mais comuns nas letras das músicas

    :param dataframe: Dataframe com multi index.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Lista com tuplas contendo as palavras mais comuns nas letras das músicas e suas frequências.
    :rtype: list

    """
    lyrics = dataframe["Track Lyrics"].str.upper()
    lyrics_list = list(dict.fromkeys(lyrics))
    words_list = []
    for lyric in lyrics_list:
        words = lyric.split()
        for word in words:
            words_list.append(word) 
    counter = collections.Counter(words_list)
    most_commom = counter.most_common(10)
    return most_commom
    
# Recebe um dataframe e retorna as 10 palavras mais comuns nas letras das músicas de cada álbum
def common_words_lyrics_album(dataframe):
    """Recebe um dataframe e retorna as 10 palavras mais comuns nas letras das músicas de cada álbum

    :param dataframe: Dataframe com 'Album Name' como parte do  multi index e com a coluna 'Track Lyrics'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Série com as 10 palavras mais comuns nas letras das músicas de cada álbum.
    :rtype: pandas.core.series.Series

    """
    new_dataframe = dataframe.groupby('Album Name').apply(common_words_by_lyrics)
    return new_dataframe

# Recebe um dataframe e retorna os 3 álbuns que mais aparecem nas letras das músicas
def album_in_lyrics(dataframe):
    """Recebe um dataframe e retorna os 3 álbuns que mais aparecem nas letras das músicas

    :param dataframe: Dataframe com 'Album Name' como parte do  multi index e com a coluna 'Track Lyrics'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com os 3 álbuns que mais aparecem nas letras das músicas.
    :rtype: pandas.core.frame.DataFrame

    """
    albuns = dataframe.index.get_level_values(0)
    albuns_series = pd.Series(albuns).str.upper()
    albuns_array = albuns_series.unique()
    words_list = []
    for album in albuns_array:
        words = album.split()
        for word in words:
            words_list.append(word) 
    lyrics = dataframe["Track Lyrics"]
    lyrics_series =  pd.Series(lyrics).str.upper()
    lyrics_array = lyrics_series.unique()
    match_dictionaty = {}
    for word in words_list:
        match_dictionaty[word] = 0
        for lyric in lyrics_array:
            match = lyric.count(word)
            match_dictionaty[word] += match
    matches_dataframe = pd.DataFrame(match_dictionaty.values(),match_dictionaty.keys(),["Frequency"])
    return matches_dataframe["Frequency"].nlargest(3)
   
# Recebe um dataframe e retorna as 3 canções que mais aparecem nas letras das músicas    
def song_in_lyrics(dataframe):
    """Recebe um dataframe e retorna as 3 canções que mais aparecem nas letras das músicas.

    :param dataframe: Dataframe com 'Track Name' como parte do  multi index e com a coluna 'Track Lyrics'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com as 3 músicas que mais aparecem nas letras das músicas.
    :rtype: pandas.core.frame.DataFrame

    """
    songs = dataframe.index.get_level_values(1)
    songs_series = pd.Series(songs).str.upper()
    songs_array = songs_series.unique()   
    words_list = []
    for song in songs_array:
        words = song.split()
        for word in words:
            words_list.append(word) 
    lyrics = dataframe["Track Lyrics"]
    lyrics_series =  pd.Series(lyrics).str.upper()
    lyrics_array = lyrics_series.unique()
    match_dictionaty = {}
    for word in words_list:
        match_dictionaty[word] = 0
        for lyric in lyrics_array:
            match = lyric.count(word)
            match_dictionaty[word] += match
    matches_dataframe = pd.DataFrame(match_dictionaty.values(),match_dictionaty.keys(),["Frequency"])
    return matches_dataframe["Frequency"].nlargest(3)

# Recebe um dataframe e retorna a popularidade média de músicas explícitas e não explícitas    
def explicit_popularity(dataframe):
    """Recebe um dataframe e retorna a popularidade média de músicas explícitas e não explícitas.

    :param dataframe: Dataframe com colunas 'Explicit' e 'Popularity'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com as popularidades médias das músicas explícitas e não explícitas.
    :rtype: pandas.core.frame.DataFrame

    """
    grouped = dataframe.groupby("Explicit")["Popularity"].mean()
    return grouped

# Recebe um dataframe e retorna o álbum mais popular com base na popularidade média de suas músicas
def most_popular_album(dataframe):
    """Recebe um dataframe e retorna o álbum mais popular com base na popularidade média de suas músicas

    :param dataframe: Dataframe com 'Album' no multi index e com coluna popularity.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com os álbuns mais populares e suas popularidades.
    :rtype: pandas.core.frame.DataFrame

    """
    mean_popularity = dataframe.groupby("Album Name")["Popularity"].mean()
    popularity_sorted= mean_popularity.sort_values(ascending=False)
    most_popular = popularity_sorted.nlargest(1,keep='all')
    return most_popular
  
# Recebe um dataframe e retorna um dicionário com os gêneros encontrados em cada álbum
def gender_album(dataframe):  
    """Recebe um dataframe e retorna um dicionário com as chaves sendo os álbuns e os valores sendo os gêneros encontrados em cada álbum.
    
    :param dataframe: Dataframe com coluna 'Genre'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dicionário com as chaves sendo os álbuns e os valores sendo os gêneros encontrados em cada álbum.
    :rtype: pandas.core.frame.DataFrame
    
    """
    grouped = dataframe.groupby(level=0)
    album_genres = {}
    for album, new_df in grouped:
        values = new_df["Genre"].values
        album_genres[album]=unique_values(values)
    return album_genres


