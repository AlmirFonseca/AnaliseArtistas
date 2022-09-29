# Análise exploratória

#Importe as bibliotecas necessárias
import pandas as pd
import numpy as np
import collections

# Imprime as 3 músicas mais ouvidas por álbum
def most_listened_by_album(dataframe):
    return dataframe.groupby('Álbum')['Popularidade'].nlargest(3,keep='all')
 
 
# Imprime as 3 músicas menos ouvidas por álbum   
def least_listened_by_album(dataframe):
    return dataframe.groupby('Álbum')['Popularidade'].nsmallest(3,keep='all')
    
# Imprime as 3 músicas mais longas por álbum
def longest_by_album(dataframe):
    return dataframe.groupby('Álbum')['Duração'].nlargest(3,keep='all')
    
# Imprime as 3 músicas menos longas por álbum
def shortest_by_album(dataframe):
    return dataframe.groupby('Álbum')['Duração'].nsmallest(3,keep='all')
   
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
    
# Imprime as 3 palavras mais comuns nos títulos dos álbuns
def common_words_by_album(dataframe):
    albuns = dataframe.index.get_level_values(0)
    albuns_list = list(dict.fromkeys(albuns))
    words_list = []
    for album in albuns_list:
        words = album.split()
        for word in words:
            words_list.append(word) 
    counter = collections.Counter(words_list)
    most_commom = counter.most_common(3)
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
    most_commom = counter.most_common(3)
    return most_commom
    
    
# Imprime as 10 palavras mais comuns nas letras das músicas
def palavra_comuns_letras(dataframe):
    letras = dataframe["Letras"]
    lista_letras = list(dict.fromkeys(letras))
    lista_palavras = []
    for letra in lista_letras:
        palavras = letra.split()
        for palavra in palavras:
            lista_palavras.append(palavra) 
    contador = collections.Counter(lista_palavras)
    mais_comuns = contador.most_common(10)
    print(mais_comuns)
    
# Imprime as 10 palavras mais comuns nas letras de cada álbum
def letras_comuns_album(dataframe):
    dataframe.groupby('Álbum').apply(palavra_comuns_letras)
    

    
