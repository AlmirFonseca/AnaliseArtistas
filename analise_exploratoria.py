########################### Análise exploratória ##############################

#Importe as bibliotecas necessárias
import pandas as pd
import numpy as np
import collections

# Recebe um dataframe e retorna as 3 músicas mais ouvidas por álbum
def most_listened_by_album(dataframe):
    grouped = dataframe.groupby('Album')['Popularity'].nlargest(3,keep='all') # Agrupa por 'Album' e seleciona os 3 maiores valores da coluna 'Popularity'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album',inplace = True)
    return grouped

# Recebe um dataframe e retorna as 3 músicas menos ouvidas por álbum  
def least_listened_by_album(dataframe):
    grouped = dataframe.groupby('Album')['Popularity'].nsmallest(3,keep='all')# Agrupa por 'Album' e seleciona os 3 menores valores da coluna 'Popularity'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album',inplace = True)
    return grouped
    
# Recebe um dataframe e retorna as 3 músicas mais longas por álbum  
def longest_by_album(dataframe):
    grouped = dataframe.groupby('Album')['Duration'].nlargest(3,keep='all')# Agrupa por 'Album' e seleciona os 3 maiores valores da coluna 'Duration'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album',inplace = True)
    return grouped
    
# Recebe um dataframe e retorna as 3 músicas menos longas por álbum
def shortest_by_album(dataframe):
    grouped = dataframe.groupby('Album')['Duration'].nsmallest(3,keep='all')# Agrupa por 'Album' e seleciona os 3 menores valores da coluna 'Duration'
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Album',inplace = True)
    return grouped

# Recebe um dataframe e retorna as 3 músicas mais ouvidas na história do artista
def most_listened(dataframe):
    return dataframe.nlargest(3, 'Popularity',keep='all')

# Recebe um dataframe e retorna as 3 músicas menos ouvidas na história do artista
def least_listened(dataframe):
    return dataframe.nsmallest(3, 'Popularity',keep='all')

# Recebe um dataframe e retorna as 3 músicas mais longas na história do artista
def longest(dataframe):
    return dataframe.nlargest(3, 'Duration',keep='all')
    
# Recebe um dataframe e retorna as 3 músicas menos longas na história do artista
def shortest(dataframe):
    return dataframe.nsmallest(3, 'Duration',keep='all')

# Recebe uma lista com alguns itens separados por '/' e retorna um array com valores únicos
def unique_values(array):
    unique_values_array = []
    for i in range(len(array)):
        array_item = array[i].split("/")
        for item in array_item:
            unique_values_array.append(item)
    unique_values_array = np.asarray(unique_values_array)
    unique_values_array = np.unique(unique_values_array)
    return unique_values_array 

def albuns_awards(dataframe):
    grouped = dataframe.groupby(level=0)
    dictionary_quantity_awards = {}
    for album, album_dataframe in grouped:
        awards = album_dataframe["Awards"].values
        dictionary_quantity_awards[album]=len(unique_values(awards))
    quantity_awards_dataframe = pd.DataFrame(dictionary_quantity_awards.values(),dictionary_quantity_awards.keys(),columns=["Awards"])
    most_recognized = quantity_awards_dataframe.nlargest(1,'Awards')
    return most_recognized

# Recebe um dataframe e retorna a correlação de Pearson entre duração e popularidade das músicas
def duration_popularity(dataframe):
    correlation = dataframe.corr(method ='pearson')
    return correlation.loc["Duration","Popularity"]
  
# Recebe um dataframe e retorna as 10 palavras mais comuns nos títulos dos álbuns
def common_words_by_album(dataframe):
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
    new_dataframe = dataframe.groupby('Album').apply(common_words_by_lyrics)
    return new_dataframe


# Recebe um dataframe e retorna os 3 álbuns que mais aparecem nas letras das músicas
def album_in_lyrics(dataframe):
    albuns = dataframe.index.get_level_values(0)
    albuns_series = pd.Series(albuns).str.upper()
    albuns_array = albuns_series.unique()   
    lyrics = dataframe["Lyrics"]
    lyrics_series =  pd.Series(lyrics).str.upper()
    lyrics_array = lyrics_series.unique()
    match_dictionaty = {}
    for album in albuns_array:
        match_dictionaty[album] = 0
        for lyric in lyrics_array:
            match = lyric.count(album)
            match_dictionaty[album] += match
    matches_dataframe = pd.DataFrame(match_dictionaty.values(),match_dictionaty.keys(),["Frequency"])
    return matches_dataframe["Frequency"].nlargest(3)
   
# Recebe um dataframe e retorna as 3 canções que mais aparecem nas letras das músicas    
def song_in_lyrics(dataframe):
    songs = dataframe.index.get_level_values(1)
    songs_series = pd.Series(songs).str.upper()
    songs_array = songs_series.unique()   
    lyrics = dataframe["Lyrics"]
    lyrics_series =  pd.Series(lyrics).str.upper()
    lyrics_array = lyrics_series.unique()
    match_dictionaty = {}
    for song in songs_array:
        match_dictionaty[song] = 0
        for lyric in lyrics_array:
            match = lyric.count(song)
            match_dictionaty[song] += match
    matches_dataframe = pd.DataFrame(match_dictionaty.values(),match_dictionaty.keys(),["Frequency"])
    return matches_dataframe["Frequency"].nlargest(3)

# Recebe um dataframe e retorna a popularidade média de músicas explícitas e não explícitas    
def explicit_popularity(dataframe):
    grouped = dataframe.groupby("Explicit")["Popularity"].mean()
    return grouped


# Recebe um dataframe e retorna o álbum mais popular com base na popularidade média de suas músicas
def most_popular_album(dataframe):
    mean_popularity = dataframe.groupby("Album")["Popularity"].mean()
    popularity_sorted= mean_popularity.sort_values(ascending=False)
    most_popular = popularity_sorted.nlargest(1,keep='all')
    return most_popular

# Recebe um dataframe e retorna um dicionário com os gêneros encontrados em cada álbum
def gender_album(dataframe):  
    grouped = dataframe.groupby(level=0)
    album_genres = {}
    for album, new_df in grouped:
        values = new_df["Genre"].values
        album_genres[album]=unique_values(values)
    return album_genres
