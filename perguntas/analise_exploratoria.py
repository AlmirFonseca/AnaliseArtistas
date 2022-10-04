''' Módulo de Análise exploratória 

Esse módulo contém funções responsáveis por responder perguntas a partir da análise de dataframes musicais em um formato específico.
O formato do dataframe deve ser igual ao gerado pelo módulo database nesse mesmo repositório e lido pela função create_dataframe.

'''

#Importe as bibliotecas necessárias
import pandas as pd
import numpy as np
import collections


# Recebe um dataframe e retorna as 3 músicas mais ouvidas por álbum
def most_listened_by_album(dataframe):
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas mais ouvidas por álbum
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame com 'Album' como parte do multi index e com coluna 'Popularity'.

    Returns
    -------
    grouped : pandas.core.frame.DataFrame
        DataFrame com 3 músicas mais ouvidas por álbum, caso haja mais músicas com a mesma popularidade, todas serão retornadas.

    '''
    grouped = dataframe.groupby('Album')['Popularity'].nlargest(3,keep='all') # Agrupa por 'Album' e seleciona os 3 maiores valores da coluna 'Popularity'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album',inplace = True)
    return grouped

# Recebe um dataframe e retorna as 3 músicas menos ouvidas por álbum  
def least_listened_by_album(dataframe):
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas menos ouvidas por álbum
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame com 'Album' como parte do multi index e com coluna 'Popularity'.

    Returns
    -------
    grouped : pandas.core.frame.DataFrame
        DataFrame com 3 músicas menos ouvidas por álbum, caso haja mais músicas com a mesma popularidade, todas serão retornadas.

    '''
    grouped = dataframe.groupby('Album')['Popularity'].nsmallest(3,keep='all') # Agrupa por 'Album' e seleciona os 3 menores valores da coluna 'Popularity'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album',inplace = True)
    return grouped
    
# Recebe um dataframe e retorna as 3 músicas mais longas por álbum  
def longest_by_album(dataframe):
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas mais longas por álbum
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame com 'Album' como parte do multi index e com coluna 'Duration'.

    Returns
    -------
    grouped : pandas.core.frame.DataFrame
        DataFrame com 3 músicas mais longas por álbum, caso haja mais músicas com a mesma duração, todas serão retornadas.

    '''  
    grouped = dataframe.groupby('Album')['Duration'].nlargest(3,keep='all') # Agrupa por 'Album' e seleciona os 3 maiores valores da coluna 'Duration'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album',inplace = True)
    return grouped
    
# Recebe um dataframe e retorna as 3 músicas menos longas por álbum
def shortest_by_album(dataframe):
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas menos longas por álbum
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame com 'Album' como parte do multi index e com coluna 'Duration'.

    Returns
    -------
    grouped : pandas.core.frame.DataFrame
        DataFrame com 3 músicas menos longas por álbum, caso haja mais músicas com a mesma duração, todas serão retornadas.

    '''  
    grouped = dataframe.groupby('Album')['Duration'].nsmallest(3,keep='all') # Agrupa por 'Album' e seleciona os 3 menores valores da coluna 'Duration'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album',inplace = True)
    return grouped

# Recebe um dataframe e retorna as 3 músicas mais ouvidas na história do artista
def most_listened(dataframe):
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas mais populares
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame com coluna 'Popularity'.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame com 3 músicas mais populares, caso haja mais músicas com a mesma popularidade, todas serão retornadas.

    '''  
    return dataframe.nlargest(3, 'Popularity',keep='all')

# Recebe um dataframe e retorna as 3 músicas menos ouvidas na história do artista
def least_listened(dataframe):
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas menos populares
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame com coluna 'Popularity'.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame com 3 músicas menos populares, caso haja mais músicas com a mesma popularidade, todas serão retornadas.

    '''  
    return dataframe.nsmallest(3, 'Popularity',keep='all')

# Recebe um dataframe e retorna as 3 músicas mais longas na história do artista
def longest(dataframe):
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas mais longas
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame com coluna 'Duration'.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame com 3 músicas mais longas, caso haja mais músicas com a mesma duração, todas serão retornadas.

    '''  
    return dataframe.nlargest(3, 'Duration',keep='all')
    
# Recebe um dataframe e retorna as 3 músicas menos longas na história do artista
def shortest(dataframe):
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas mais curtas
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame com coluna 'Duration'.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame com 3 músicas mais curtas, caso haja mais músicas com a mesma duração, todas serão retornadas.

    '''  
    return dataframe.nsmallest(3, 'Duration',keep='all')

# Recebe uma lista com algumas strings contendo itens separados por '/' e retorna um array com valores únicos dos itens
def unique_values(array):
    '''
    Recebe uma lista com algumas strings contendo itens separados por '/' e retorna um array com valores únicos dos itens
    Parameters
    ----------
    array : list
        Lista com alguns itens sendo palavras separadas por '/'.

    Returns
    -------
    unique_values_array : np.ndarray
        Array com todas as palavras contidas no array de input, incluindo as separadas por '/'. Toda palavra só aparecerá uma única vez.

    '''
    
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
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 álbuns mais premiados e suas quantidades de prêmios
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame com coluna 'Duration'.

    Returns
    -------
    most_recognized : pandas.core.frame.DataFrame
        Dataframe com os álbuns mais premiados e a quantidade de prêmios recebidos.

    '''
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
    '''
    Recebe um dataframe no formato pandas e retorna um dataframe com as 3 álbuns mais premiados e suas quantidades de prêmios
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        Dataframe com as colunas Duration e Popularity.

    Returns
    -------
    numpy.float64
        Correlação entre as colunas Duration e Popularity.

    '''
    correlation = dataframe.corr(method ='pearson')
    return correlation.loc["Duration","Popularity"]

# Recebe um dataframe e retorna as 10 palavras mais comuns nos títulos dos álbuns
def common_words_by_album(dataframe):
    '''
    Recebe um dataframe e retorna as 10 palavras mais comuns nos títulos dos álbuns
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        Dataframe com multi index.

    Returns
    -------
    most_commom : list
        Lista com tuplas contendo as palavras mais comuns nos títulos dos álbuns e suas frequências.

    '''
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
    '''
    Recebe um dataframe e retorna as 10 palavras mais comuns nos títulos das músicas
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        Dataframe com multi index.

    Returns
    -------
    most_commom : list
        Lista com tuplas contendo as palavras mais comuns nos títulos das músicas e suas frequências.

    '''
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
    '''
    
    Recebe um dataframe e retorna as 10 palavras mais comuns nas letras das músicas
    dataframe : pandas.core.frame.DataFrame
        Dataframe com multi index.

    Returns
    -------
    most_commom : list
        Lista com tuplas contendo as palavras mais comuns nas letras das músicas e suas frequências.

    '''
    lyrics = dataframe["Lyrics"].str.upper()
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
    '''
    
    Recebe um dataframe e retorna as 10 palavras mais comuns nas letras das músicas de cada álbum
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        Dataframe com 'Album' como parte do  multi index e com a coluna 'Lyrics'.

    Returns
    -------
    new_dataframe : pandas.core.series.Series
        Série com as 10 palavras mais comuns nas letras das músicas de cada álbum.

    '''
    new_dataframe = dataframe.groupby('Album').apply(common_words_by_lyrics)
    return new_dataframe

# Recebe um dataframe e retorna os 3 álbuns que mais aparecem nas letras das músicas
def album_in_lyrics(dataframe):
    '''
    
    Recebe um dataframe e retorna os 3 álbuns que mais aparecem nas letras das músicas
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        Dataframe com 'Album' como parte do  multi index e com a coluna 'Lyrics'.

    Returns
    -------
    pandas.core.frame.DataFrame
        Dataframe com os 3 álbuns que mais aparecem nas letras das músicas

    '''
    albuns = dataframe.index.get_level_values(0)
    albuns_series = pd.Series(albuns).str.upper()
    albuns_array = albuns_series.unique()
    words_list = []
    for album in albuns_array:
        words = album.split()
        for word in words:
            words_list.append(word) 
    lyrics = dataframe["Lyrics"]
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
    '''
    
    Recebe um dataframe e retorna as 3 canções que mais aparecem nas letras das músicas 
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        Dataframe com 'Album' como parte do  multi index e com a coluna 'Lyrics'.

    Returns
    -------
    pandas.core.frame.DataFrame
        Dataframe com as 3 músicas que mais aparecem nas letras das músicas

    '''
    songs = dataframe.index.get_level_values(1)
    songs_series = pd.Series(songs).str.upper()
    songs_array = songs_series.unique()   
    words_list = []
    for song in songs_array:
        words = song.split()
        for word in words:
            words_list.append(word) 
    lyrics = dataframe["Lyrics"]
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
    '''
    
    Recebe um dataframe e retorna a popularidade média de músicas explícitas e não explícitas  
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        Dataframe com colunas 'Explicit' e 'Popularity'.

    Returns
    -------
    grouped = pandas.core.frame.DataFrame
        Dataframe com as popularidades das músicas explícitas e não explícitas.

    '''
    grouped = dataframe.groupby("Explicit")["Popularity"].mean()
    return grouped

# Recebe um dataframe e retorna o álbum mais popular com base na popularidade média de suas músicas
def most_popular_album(dataframe):
    '''
    
    Recebe um dataframe e retorna o álbum mais popular com base na popularidade média de suas músicas
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        Dataframe com 'Album' no multi index e com coluna popularity.

    Returns
    -------
    most_popular : pandas.core.frame.DataFrame
        Dataframe com os álbuns mais populares e suas popularidades.

    '''
    mean_popularity = dataframe.groupby("Album")["Popularity"].mean()
    popularity_sorted= mean_popularity.sort_values(ascending=False)
    most_popular = popularity_sorted.nlargest(1,keep='all')
    return most_popular
  
# Recebe um dataframe e retorna um dicionário com os gêneros encontrados em cada álbum
def gender_album(dataframe):  
    '''
    Recebe um dataframe no formato pandas e retorna um dicionário com os gêneros encontrados em cada álbum
    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        Dataframe com coluna 'Genre'.

    Returns
    -------
    album_genres : dict
        Dicionário com os álbuns sendo as chaves e os valores sendo um array contendo os gêneros daquele álbum.

    '''
    grouped = dataframe.groupby(level=0)
    album_genres = {}
    for album, new_df in grouped:
        values = new_df["Genre"].values
        album_genres[album]=unique_values(values)
    return album_genres


