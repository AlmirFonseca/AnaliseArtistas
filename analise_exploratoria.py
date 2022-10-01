# Análise exploratória

#Importe as bibliotecas necessárias
import pandas as pd
import numpy as np
import collections

# Imprime as 3 músicas mais ouvidas por álbum
def most_listened_by_album(dataframe):
    grouped = dataframe.groupby('Álbum')['Popularidade'].nlargest(3,keep='all')
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Álbum',inplace = True)
    return grouped


# Imprime as 3 músicas menos ouvidas por álbum   
def least_listened_by_album(dataframe):
    grouped = dataframe.groupby('Álbum')['Popularidade'].nsmallest(3,keep='all')
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Álbum',inplace = True)
    return grouped
    
# Imprime as 3 músicas mais longas por álbum
def longest_by_album(dataframe):
    grouped = dataframe.groupby('Álbum')['Duração'].nlargest(3,keep='all')
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Álbum',inplace = True)
    return grouped
    
# Imprime as 3 músicas menos longas por álbum
def shortest_by_album(dataframe):
    grouped = dataframe.groupby('Álbum')['Duração'].nsmallest(3,keep='all')
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns='Álbum',inplace = True)
    return grouped
   
# Imprime as 3 músicas mais ouvidas na história do artista
def most_listened(dataframe):
    return dataframe.nlargest(3, 'Popularidade',keep='all')

# Imprime as 3 músicas menos ouvidas na história do artista
def least_listened(dataframe):
    return dataframe.nsmallest(3, 'Popularidade',keep='all')

# Imprime as 3 músicas mais longas na história do artista
def longest(dataframe):
    return dataframe.nlargest(3, 'Duração',keep='all')
    
# Imprime as 3 músicas menos longas na história do artista
def shortest(dataframe):
    return dataframe.nsmallest(3, 'Duração',keep='all')
 
# Imprime a correlação de Pearson entre Duração e Popularidade
def duration_popularity(dataframe):
    correlation = dataframe.corr(method ='pearson')
    return correlation.loc["Duração","Popularidade"]
    
# Imprime as 10 palavras mais comuns nos títulos dos álbuns
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
    
    
# Imprime as 3 palavras mais comuns nos títulos das músicas
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
    
    
# Imprime as 10 palavras mais comuns nas letras das músicas
def common_words_by_lyrics(dataframe):
    lyrics = dataframe["Letras"].str.upper()
    lyrics_list = list(dict.fromkeys(lyrics))
    words_list = []
    for lyric in lyrics_list:
        words = lyric.split()
        for word in words:
            words_list.append(word) 
    counter = collections.Counter(words_list)
    most_commom = counter.most_common(10)
    return most_commom
    
# Imprime as 10 palavras mais comuns nas letras de cada álbum
def common_words_lyrics_album(dataframe):
    new_dataframe = dataframe.groupby('Álbum').apply(common_words_by_lyrics)
    return new_dataframe

# Retorna o álbum mais popular com base na popularidade média de suas músicas
def most_popular_album(dataframe):
    mean_popularity = dataframe.groupby("Álbum")["Popularidade"].mean()
    popularity_sorted= mean_popularity.sort_values(ascending=False)
    most_popular = popularity_sorted.nlargest(1,keep='all')
    return most_popular

# Retorna os 3 álbuns que mais aparecem nas letras das músicas
def album_in_lyrics(dataframe):
    albuns = dataframe.index.get_level_values(0)
    albuns_series = pd.Series(albuns).str.upper()
    albuns_array = albuns_series.unique()   
    lyrics = dataframe["Letras"]
    lyrics_series =  pd.Series(lyrics).str.upper()
    lyrics_array = lyrics_series.unique()
    match_dictionaty = {}
    for album in albuns_array:
        match_dictionaty[album] = 0
        for lyric in lyrics_array:
            match = lyric.count(album)
            match_dictionaty[album] += match
    matches_dataframe = pd.DataFrame(match_dictionaty.values(),match_dictionaty.keys(),["Frequência"])
    return matches_dataframe["Frequência"].nlargest(3)
   
# Retorna as 3 canções que mais aparecem nas letras das músicas    
def song_in_lyrics(dataframe):
    songs = dataframe.index.get_level_values(1)
    songs_series = pd.Series(songs).str.upper()
    songs_array = songs_series.unique()   
    lyrics = dataframe["Letras"]
    lyrics_series =  pd.Series(lyrics).str.upper()
    lyrics_array = lyrics_series.unique()
    match_dictionaty = {}
    for song in songs_array:
        match_dictionaty[song] = 0
        for lyric in lyrics_array:
            match = lyric.count(song)
            match_dictionaty[song] += match
    matches_dataframe = pd.DataFrame(match_dictionaty.values(),match_dictionaty.keys(),["Frequência"])
    return matches_dataframe["Frequência"].nlargest(3)

    
