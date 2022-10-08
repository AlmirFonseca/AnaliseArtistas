"""Módulo de análise exploratória

Esse módulo contém funções responsáveis por responder perguntas a partir da análise de dataframes em um formato específico.
O formato do dataframe deve ser igual ao gerado pelo módulo database nesse mesmo repositório e lido pela função create_dataframe.

"""

#Importe as bibliotecas necessárias
import collections
import re
import numpy as np
import pandas as pd

# Recebe um dataframe e retorna as 3 músicas mais ouvidas por álbum
def most_listened_by_album(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas mais ouvidas por álbum.

    :param dataframe: DataFrame com ``Album Name`` como parte do multi index e com coluna ``Popularity``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas mais ouvidas por álbum, caso haja mais músicas com a mesma popularidade, todas serão retornadas.
    :rtype: `pandas.core.frame.DataFrame`

    """
    grouped = dataframe.groupby("Album Name")["Popularity"].nlargest(3,keep="all") # Agrupa por "Album Name" e seleciona os 3 maiores valores da coluna "Popularity"
    grouped = grouped.reset_index(level = 0) 
    grouped.drop(columns="Album Name",inplace = True)
    return grouped

# Recebe um dataframe e retorna as 3 músicas menos ouvidas por álbum  
def least_listened_by_album(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas menos ouvidas por álbum.
    
    :param dataframe: DataFrame com ``Album Name`` como parte do multi index e com coluna ``Popularity``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas menos ouvidas por álbum, caso haja mais músicas com a mesma popularidade, todas serão retornadas.
    :rtype: `pandas.core.frame.DataFrame`

    """
    grouped = dataframe.groupby("Album Name")["Popularity"].nsmallest(3,keep="all") # Agrupa por "Album Name" e seleciona os 3 menores valores da coluna "Popularity"
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns="Album Name",inplace = True)
    return grouped

def longest_by_album(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas mais longas por álbum.

    :param dataframe: DataFrame com ``Album Name`` como parte do multi index e com coluna ``Duration``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas mais longas por álbum, caso haja mais músicas com a mesma duração, todas serão retornadas.
    :rtype: `pandas.core.frame.DataFrame`

    """
    grouped = dataframe.groupby("Album Name")["Duration Seconds"].nlargest(3,keep="all") # Agrupa por "Album Name" e seleciona os 3 maiores valores da coluna "Duration Seconds"
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns="Album Name",inplace = True)
    return grouped
    
# Recebe um dataframe e retorna as 3 músicas menos longas por álbum
def shortest_by_album(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas mais curtas por álbum.

    :param dataframe: DataFrame com ``Album Name`` como parte do multi index e com coluna ``Duration Seconds``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas mais curtas por álbum, caso haja mais músicas com a mesma popularidade, todas serão retornadas.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    grouped = dataframe.groupby("Album Name")["Duration Seconds"].nsmallest(3,keep="all") # Agrupa por "Album Name" e seleciona os 3 menores valores da coluna "Duration"
    grouped = grouped.reset_index(level = 0)
    grouped.drop(columns="Album Name",inplace = True)
    return grouped

# Recebe um dataframe e retorna as 3 músicas mais ouvidas na história do artista
def most_listened(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas mais ouvidas.
    
    :param dataframe: DataFrame com coluna ``Popularity``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas mais ouvidas, caso haja mais músicas com a mesma popularidade, todas serão retornadas.
    :rtype: `pandas.core.frame.DataFrame`
    
    """ 
    return dataframe.nlargest(3, "Popularity",keep="all")

# Recebe um dataframe e retorna as 3 músicas menos ouvidas na história do artista
def least_listened(dataframe):
    """Recebe um dataframe e o retorna com um filtro para indicar as 3 músicas menos ouvidas. 
    
    :param dataframe: DataFrame com coluna ``Popularity``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com as 3 músicas menos ouvidas, caso haja mais músicas com a mesma popularidade, todas serão retornadas..
    :rtype: `pandas.core.frame.DataFrame`
    
    """ 
    return dataframe.nsmallest(3, "Popularity",keep="all")

# Recebe um dataframe e retorna as 3 músicas mais longas na história do artista
def longest(dataframe):
    """Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas mais longas.
    
    :param dataframe: DataFrame com coluna ``Duration Seconds``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com 3 músicas mais longas, caso haja mais músicas com a mesma duração, todas serão retornadas.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    return dataframe.nlargest(3, "Duration Seconds",keep="all")
    
# Recebe um dataframe e retorna as 3 músicas menos longas na história do artista
def shortest(dataframe):
    """Recebe um dataframe no formato pandas e retorna um dataframe com as 3 músicas mais curtas.
    
    :param dataframe: DataFrame com coluna ``Duration Seconds``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: DataFrame com 3 músicas mais curtas, caso haja mais músicas com a mesma duração, todas serão retornadas.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    return dataframe.nsmallest(3, "Duration Seconds",keep="all")

# Recebe uma lista com algumas strings contendo itens separados por "/" e retorna um array com valores únicos dos itens
def unique_values(array):
    """Recebe uma lista com algumas strings contendo itens separados por ``/`` e retorna um array com valores únicos dos itens.
    
    :param array: Lista com alguns itens sendo palavras separadas por ``/``.
    :type array: list
    :return: Array com todas as palavras contidas no array de input, incluindo as separadas por ``/``. Toda palavra só aparecerá uma única vez.
    :rtype: `np.ndarray`
    
    """
    unique_values_array = [] 
    for i in range(len(array)):
        array_item = array[i].split("/") # Separa as strings que contém informações separadas por "/" e cria um lista com essas informações
        for item in array_item:
            unique_values_array.append(item) # Adicione cada item da nova lista a uma lista vazia
    unique_values_array = np.asarray(unique_values_array)
    unique_values_array = np.unique(unique_values_array) # Filtra para que só haja palavras únicas
    return unique_values_array

# Recebe uma dataframe e retorna os 3 álbuns com mais prêmios
def albuns_awards(dataframe):
    """Recebe um dataframe no formato pandas e retorna um dataframe com as 3 álbuns mais premiados e suas quantidades de prêmios.
    
    :param dataframe: DataFrame com multi index e com coluna ``Awards``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com os álbuns mais premiados e a quantidade de prêmios recebidos.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    grouped = dataframe.groupby(level=0) #Agrupa o dataframe pelo index "Album Name"
    dictionary_quantity_awards = {}
    for album, album_dataframe in grouped: #Itera o dataframe agrupado 
        awards = album_dataframe["Awards"].values # Armazena os prêmios de um único álbum
        dictionary_quantity_awards[album]=len(unique_values(awards)) # Utiliza a função "unique_values" para obter um array com os prêmio dos álbuns e armazena o tamanho desse array 
    quantity_awards_dataframe = pd.DataFrame(dictionary_quantity_awards.values(),dictionary_quantity_awards.keys(),columns=["Awards"]) #Cria um novo dataframe com os álbuns e suas quantidades de prêmios.
    most_recognized = quantity_awards_dataframe.nlargest(3,"Awards") # Filtra os três álbuns mais premiados.
    return most_recognized


# Recebe um dataframe e retorna a correlação de Pearson entre duração e popularidade das músicas
def duration_popularity(dataframe):
    """Recebe um dataframe no formato pandas e retorna um float com a correlação de pearson entre duração e popularidade.
    
    :param dataframe: Dataframe com as colunas ``Duration Seconds`` e ``Popularity``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Correlação de pearson entre as colunas Duration Seconds e Popularity.
    :rtype: `numpy.float64`
    
    """
    correlation = dataframe.corr(method ="pearson")
    return correlation.loc["Duration Seconds","Popularity"]

# Remove stop words (palavras pouco significativas) de uma lista de palavras
def remove_stop_words(word_list):
    """Remove de uma lista de palavras, palavras pouco significativas da língua inglesa.

    :param word_list: Lista com palavras a serem analisadas
    :type word_list: list
    :return: Lista com palavras já filtradas
    :rtype: list
    """
    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
                  'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
                  'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                  'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                  'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
                  'when','where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
                  'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
                  'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
                  "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't","oh","i'm","oh,","don't","that's","could","me,","ep","oh,","live"]
    useful_words = []
    for word in word_list: # Itera a lista de palavras
        if word.lower() not in stop_words: 
         useful_words.append(word) # Caso a palavraa não seja um stop word a adiciona na lista useful_words
    return useful_words
            


# Recebe um dataframe e retorna as 50 palavras mais comuns nos títulos dos álbuns
def common_words_by_album(dataframe):
    """Recebe um dataframe e retorna as 50 palavras mais comuns nos títulos dos álbuns.
    
    :param dataframe: Dataframe com multi index.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Lista com tuplas contendo as palavras mais comuns nos títulos dos álbuns e suas frequências.
    :rtype: `list`
    
    """
    albuns = dataframe.index.get_level_values(0)
    albuns_list = list(dict.fromkeys(albuns)) #Cria uma lista com o nome dos álbuns
    words_list = [] 
    for album in albuns_list:
        album = str(album)
        album = re.sub("[^A-Za-z0-9]+"," ", album) #Retira caracteres não-alfabéticos dos nomes dos álbuns
        words = album.split() # Separa o nome dos álbuns em palavras
        for word in words:
            words_list.append(word) #Adiciona a palavra a uma lista vazia
    words_list = remove_stop_words(words_list) #Remove palavras não significativas
    counter = collections.Counter(words_list) #Conta a frequência de cada palavra
    most_commom = counter.most_common(50) #Retorna as 50 mais frequentes
    return most_commom
    
# Recebe um dataframe e retorna as 50 palavras mais comuns nos títulos das músicas
def common_words_by_song(dataframe):
    """Recebe um dataframe e retorna as 50 palavras mais comuns nos títulos das músicas.
    
    :param dataframe: Dataframe com multi index.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Lista com tuplas contendo as palavras mais comuns nos títulos das músicas e suas frequências.
    :rtype: `list`
    
    """
    songs = dataframe.index.get_level_values(1)
    songs_list = list(dict.fromkeys( songs))#Cria uma lista com o nome das músicas
    words_list = []
    for song in songs_list:
        song = str(song)
        song = re.sub("[^A-Za-z0-9]+"," ", song)#Retira caracteres não-alfabéticos dos nomes das músicas
        words = song.split()# Separa o nome das músicas em palavras
        for word in words:
            words_list.append(word) 
    words_list = remove_stop_words(words_list)#Remove palavras não significativas
    counter = collections.Counter(words_list) #Conta a frequência de cada palavra
    most_commom = counter.most_common(50) #Retorna as 50 mais frequentes
    return most_commom
    
# Recebe um dataframe e retorna as 50 palavras mais comuns nas letras das músicas
def common_words_by_lyrics(dataframe):
    """Recebe um dataframe e retorna as 50 palavras mais comuns nas letras das músicas.
    
    :param dataframe: Dataframe com multi index.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Lista com tuplas contendo as palavras mais comuns nas letras das músicas e suas frequências.
    :rtype: `list`
    
    """
    lyrics = dataframe["Track Lyrics"].str.upper()
    lyrics_list = list(dict.fromkeys(lyrics))#Cria uma lista com as letras das músicas
    words_list = []
    for lyric in lyrics_list:
        lyric = str(lyric)
        lyric = re.sub("[^A-Za-z0-9]+"," ", lyric)#Retira caracteres não-alfabéticos das letras das músicas
        words = lyric.split()# Separa as letras das músicas em palavras
        for word in words:
            words_list.append(word)
    words_list = remove_stop_words(words_list)#Remove palavras não significativas
    counter = collections.Counter(words_list)#Conta a frequência de cada palavra
    most_commom = counter.most_common(50) #Retorna as 50 mais frequentes
    return most_commom
    
# Recebe um dataframe e retorna as 50 palavras mais comuns nas letras das músicas de cada álbum
def common_words_lyrics_album(dataframe):
    """Recebe um dataframe e retorna as 50 palavras mais comuns nas letras das músicas de cada álbum.
    
    :param dataframe: Dataframe com ``Album Name`` como parte do  multi index e com a coluna ``Track Lyrics``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Série com as 50 palavras mais comuns nas letras das músicas de cada álbum.
    :rtype: `pandas.core.series.Series`
    
    """
    new_dataframe = dataframe.groupby("Album Name").apply(common_words_by_lyrics)
    return new_dataframe

# Recebe um dataframe e retorna os 3 álbuns que mais aparecem nas letras das músicas
def album_in_lyrics(dataframe):
    """Recebe um dataframe e retorna os 3 álbuns que mais aparecem nas letras das músicas.
    
    :param dataframe: Dataframe com ``Album Name`` como parte do  multi index e com a coluna ``Track Lyrics``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com os 3 álbuns que mais aparecem nas letras das músicas.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    albuns = dataframe.index.get_level_values(0)
    albuns_series = pd.Series(albuns).str.upper()
    albuns_array = albuns_series.unique() # Cria uma série com o nome dos álbuns
    words_list = []
    for album in albuns_array:
        album = str(album)
        album = re.sub("[^A-Za-z0-9]+"," ", album) #Retira caracteres não-alfabéticos do nome dos álbuns
        words = album.split() # Separa o nome do álbum em uma lista de palavras
        for word in words:
            words_list.append(word) #Adiciona cada palavra a uma lista vazia
    words_list = remove_stop_words(words_list) #Remove palavras não significativas
    lyrics = dataframe["Track Lyrics"]
    lyrics_series =  pd.Series(lyrics).str.upper()
    lyrics_array = lyrics_series.unique()# Cria uma série as letras das músicas
    match_dictionaty = {}
    for word in words_list:
        word = str(word)
        word = re.sub("[^A-Za-z0-9]+"," ", word) #Garante que nenhuma palavras da "words_list" tenha caracteres especiais
        match_dictionaty[word] = 0 #Cria um dicionário que armazena a frequência das palavras dos nomes dos álbuns nas letras das músicas
        for lyric in lyrics_array:
            lyric = str(lyric)
            match = lyric.count(word) # Conta a frequência que cada palavra aparece
            match_dictionaty[word] += match # Adiciona o valor da frequência ao dicionário
    matches_dataframe = pd.DataFrame(match_dictionaty.values(),match_dictionaty.keys(),["Frequency"]) #Cria um dicionário com os matches 
    return matches_dataframe["Frequency"].nlargest(3) #Retorna as 3 palavras mais comuns que álbuns e letras tem em comum
   
# Recebe um dataframe e retorna as 3 canções que mais aparecem nas letras das músicas    
def song_in_lyrics(dataframe):
    """Recebe um dataframe e retorna as 3 canções que mais aparecem nas letras das músicas.
    
    :param dataframe: Dataframe com ``Track Name`` como parte do  multi index e com a coluna ``Track Lyrics``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com as 3 músicas que mais aparecem nas letras das músicas.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    songs = dataframe.index.get_level_values(1)
    songs_series = pd.Series(songs).str.upper()
    songs_array = songs_series.unique()  # Cria uma série com o nome das músicas
    words_list = []
    for song in songs_array:
        song = str(song)
        song = re.sub("[^A-Za-z0-9]+"," ", song)#Retira caracteres não-alfabéticos do nome das músicas
        words = song.split()# Separa o nome das músicas em uma lista de palavras
        for word in words:
            words_list.append(word) #Adiciona cada palavra a uma lista vazia
    words_list = remove_stop_words(words_list)#Remove palavras não significativas
    lyrics = dataframe["Track Lyrics"]
    lyrics_series =  pd.Series(lyrics).str.upper()
    lyrics_array = lyrics_series.unique()# Cria uma série as letras das músicas
    match_dictionaty = {}
    for word in words_list:
        match_dictionaty[word] = 0 #Cria um dicionário que armazena a frequência das palavras dos nomes das músicas nas letras das músicas
        for lyric in lyrics_array:
            lyric = str(lyric)
            lyric = re.sub("[^A-Za-z0-9]+"," ", lyric) #Garante que nenhuma palavras da "words_list" tenha caracteres especiais
            match = lyric.count(word) # Conta a frequência que cada palavra aparece
            match_dictionaty[word] += match# Adiciona o valor da frequência ao dicionário
    matches_dataframe = pd.DataFrame(match_dictionaty.values(),match_dictionaty.keys(),["Frequency"])
    return matches_dataframe["Frequency"].nlargest(3)#Retorna as 3 palavras mais comuns que faixas e letras tem em comum

# Recebe um dataframe e retorna a popularidade média de músicas explícitas e não explícitas    
def explicit_popularity(dataframe):
    """Recebe um dataframe e retorna a popularidade média de músicas explícitas e não explícitas.
    
    :param dataframe: Dataframe com colunas ``Explicit`` e ``Popularity``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com as popularidades médias das músicas explícitas e não explícitas.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    grouped = dataframe.groupby("Explicit")["Popularity"].mean()
    return grouped

# Recebe um dataframe e retorna o álbum mais popular com base na popularidade média de suas músicas
def most_popular_album(dataframe):
    """Recebe um dataframe e retorna o álbum mais popular com base na popularidade média de suas músicas.
    
    :param dataframe: Dataframe com ``Album`` no multi index e com coluna ``Popularity``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dataframe com os álbuns mais populares e suas popularidades.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    mean_popularity = dataframe.groupby("Album Name")["Popularity"].mean() #Calcula a popularidade média por álbum
    popularity_sorted= mean_popularity.sort_values(ascending=False) #Armazena em ordem crescente
    most_popular = popularity_sorted.nlargest(1,keep="all") #Sorteia o álbum mais popular
    return most_popular
  
# Recebe um dataframe e retorna um dicionário com os gêneros encontrados em cada álbum
def gender_album(dataframe):  
    """Recebe um dataframe e retorna um dicionário com as chaves sendo os álbuns e os valores sendo os gêneros encontrados em cada álbum.
    
    :param dataframe: Dataframe com coluna ``Genre``.
    :type dataframe: pandas.core.frame.DataFrame
    :return: Dicionário com as chaves sendo os álbuns e os valores sendo os gêneros encontrados em cada álbum.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    grouped = dataframe.groupby(level=0) # Agrupa o dataframe pelo índice "Album Name"
    album_genres = {}
    for album, new_df in grouped:
        values = new_df["Genre"].values #Armazena os gêneros de cada álbum
        album_genres[album]=unique_values(values) #Usa a função "unique_values" para separar o gêneros de cada álbum e adicioná-los em um dicionário.
    return album_genres
