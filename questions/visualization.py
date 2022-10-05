# Visualização
''' Módulo de Visualização

Esse módulo contém funções responsáveis por gerar gráficos a partir da análise de dataframes sobre musicas em um formato específico.
O formato do dataframe deve ser igual ao gerado pelo módulo database nesse mesmo repositório e lido pela função create_dataframe no arquivo principal (main.py).

'''

# Importe as bibliotecas necessárias
import exploratory_analysis as ae
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# Use fundo preto para os gráficos
plt.style.use("dark_background")

# Recebe um dataframe e cria um gráfico de barras para a popularidade das músicas mais ouvidas 
def most_listened_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a popularidade das músicas mais ouvidas 
    
    :param dataframe: DataFrame com coluna 'Popularity'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    data = ae.most_listened(dataframe)
    plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g')
    plot.set(title='Mais ouvidas')
    plt.savefig('../images/most_listened.png')
    plt.show()

# Recebe um dataframe e cria um gráfico de barras para a popularidade das músicas menos ouvidas       
def least_listened_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a popularidade das músicas menos ouvidas 
    
    :param dataframe: DataFrame com coluna 'Popularity'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    data = ae.least_listened(dataframe)
    plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g')
    plot.set(title='Menos ouvidas')
    plt.savefig('../images/least_listened.png')
    plt.show()

# Recebe um dataframe e cria um gráfico de barras para a duração das músicas mais longas     
def longest_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a duração das músicas mais longas 
    
    :param dataframe: DataFrame com coluna 'Duration'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    data = ae.longest(dataframe)
    plot = sns.barplot(data=data, x="Duration", y=data.index.get_level_values(1), color = 'g')
    plot.set(title='Mais longas')
    plt.savefig('../images/longest.png')
    plt.show()

# Recebe um dataframe e cria um gráfico de barras para a duração das músicas mais curtas       
def shortest_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a duração das músicas mais curtas 
    
    :param dataframe: DataFrame com coluna 'Duration'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    data = ae.shortest(dataframe)
    plot = sns.barplot(data=data, x="Duration", y=data.index.get_level_values(1), color = 'g')
    plot.set(title='Mais longas')
    plt.savefig('../images/shortest.png')
    plt.show()

# Recebe um dataframe e cria gráficos de barras para a popularidade das músicas mais ouvidas por álbum    
def most_listened_by_album_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a popularidade das músicas mais ouvidas por álbum  
    
    :param dataframe: DataFrame com 'Album Name' como parte do multi index e com a coluna 'Popularity'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    grouped = dataframe.groupby(level=0)
    for album, album_dataframe in grouped:
        data = ae.most_listened(album_dataframe)
        plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g')
        plot.set(title=f'Mais ouvidas em {album}')
        plt.savefig(f'../images/most_listened_{album}.png')
        plt.show()

# Recebe um dataframe e cria gráficos de barras para a popularidade das músicas menos ouvidas por álbum    
def least_listened_by_album_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a popularidade das músicas menos ouvidas por álbum  
    
    :param dataframe: DataFrame com 'Album Name' como parte do multi index e com a coluna 'Popularity'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    grouped = dataframe.groupby(level=0)
    for album, album_dataframe in grouped:
        data = ae.least_listened(album_dataframe)
        plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g')
        plot.set(title=f'Menos ouvidas em {album}')
        plt.savefig(f'../images/least_listened_{album}.png')
        plt.show()
        
# Recebe um dataframe e cria gráficos de barras para a duração das músicas mais longas por álbum 
def longest_by_album_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a duração das músicas mais longas por álbum  
    
    :param dataframe: DataFrame com 'Album Name' como parte do multi index e com a coluna 'Duration'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    grouped = dataframe.groupby(level=0)
    for album, album_dataframe in grouped:
        data = ae.longest(album_dataframe)
        plot = sns.barplot(data=data, x="Duration", y=data.index.get_level_values(1), color = 'g')
        plot.set(title=f'Mais longas em {album}')
        plt.savefig(f'../images/longest_{album}.png')
        plt.show()

# Recebe um dataframe e cria gráficos de barras para a duração das músicas mais longas por álbum 
def shortest_by_album_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a duração das músicas mais curtas por álbum  
    
    :param dataframe: DataFrame com 'Album Name' como parte do multi index e com a coluna 'Duration'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    grouped = dataframe.groupby(level=0)
    for album, album_dataframe in grouped:
        data = ae.shortest(album_dataframe)
        plot = sns.barplot(data=data, x="Duration", y=data.index.get_level_values(1), color = 'g')
        plot.set(title=f'Menos longas em {album}')
        plt.savefig(f'../images/shortest_{album}.png')
        plt.show()
        
# Recebe um dataframe e cria um gráfico de barras para a quantidade de prêmios dos álbuns mais premiados 
def albuns_awards_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a quantidade de prêmios dos álbuns mais premiados
    
    :param dataframe: DataFrame com a coluna 'Awards'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    data = ae.albuns_awards(dataframe)
    plot = sns.barplot(data=data, x="Awards", y=data.index,color = 'g')
    plot.set(title='Mais premiadas')
    plt.savefig('../images/awards.png')
    plt.show()

# Recebe um dataframe e cria um scatterplot que associa duração e popularidade 
def duration_popularity_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a quantidade de prêmios dos álbuns mais premiados
    
    :param dataframe: DataFrame com a coluna 'Awards'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    plot = sns.scatterplot(data=dataframe, x="Duration", y="Popularity",color = 'g')
    plot.set(title='Duração x Popularidade')
    plt.savefig('../images/duration_popularity.png')
    plt.show()

# Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nas letras 
def common_words_by_lyrics_plot(dataframe):
    """Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nas letras 
    
    :param dataframe: DataFrame com a coluna 'Track Lyrics'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    resultado = ae.common_words_by_lyrics(dataframe)
    frequency = {}
    for tupla in resultado: 
        frequency[tupla[0]] = tupla[1]
    wc = WordCloud(background_color="black", max_words=1000)
    wc.generate_from_frequencies(frequency)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('../images/common_words_by_lyrics.png')
    plt.show()

# Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos das faixas     
def common_words_by_song_plot(dataframe):
    """Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos das faixas 
    
    :param dataframe: DataFrame com a coluna 'Track Name'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    resultado = ae.common_words_by_song(dataframe)
    frequency = {}
    for tupla in resultado: 
        frequency[tupla[0]] = tupla[1]
    wc = WordCloud(background_color="black", max_words=1000)
    wc.generate_from_frequencies(frequency)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('../images/common_words_by_song.png')
    plt.show()
 
# Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos dos álbuns    
def common_words_by_album_plot(dataframe):
    """Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos dos álbuns   
    
    :param dataframe: DataFrame com a coluna 'Album Name'.
    :type dataframe: pandas.core.frame.DataFrame
    :return: None
    :rtype: None
    
    """
    resultado = ae.common_words_by_album(dataframe)
    frequency = {}
    for tupla in resultado: 
        frequency[tupla[0]] = tupla[1]
    wc = WordCloud(background_color="black", max_words=1000)
    wc.generate_from_frequencies(frequency)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('./images/common_words_by_album.png')
    plt.show()
