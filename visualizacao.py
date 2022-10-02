# Visualização

# Importe as bibliotecas necessárias
import Analise_exploratoria as ae
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
    data = ae.most_listened(dataframe)
    plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g')
    plot.set(title='Mais ouvidas')
    plt.show()

# Recebe um dataframe e cria um gráfico de barras para a popularidade das músicas menos ouvidas       
def least_listened_plot(dataframe):
    data = ae.least_listened(dataframe)
    plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g')
    plot.set(title='Menos ouvidas')
    plt.show()

# Recebe um dataframe e cria um gráfico de barras para a duração das músicas mais longas     
def longest_plot(dataframe):
    data = ae.longest(dataframe)
    plot = sns.barplot(data=data, x="Duration", y=data.index.get_level_values(1), color = 'g')
    plot.set(title='Mais longas')
    plt.show()

# Recebe um dataframe e cria um gráfico de barras para a duração das músicas menos longas       
def shortest_plot(dataframe):
    data = ae.shortest(dataframe)
    plot = sns.barplot(data=data, x="Duration", y=data.index.get_level_values(1), color = 'g')
    plot.set(title='Mais longas')
    plt.show()

# Recebe um dataframe e cria gráficos de barras para a popularidade das músicas mais ouvidas por álbum    
def most_listened_by_album_plot(dataframe):
    grouped = dataframe.groupby(level=0)
    for album, album_dataframe in grouped:
        plot = sns.barplot(data=album_dataframe, x="Popularity", y=album_dataframe.index.get_level_values(1), color = 'g')
        plot.set(title=f'Mais ouvidas em {album}')
        plt.show()

# Recebe um dataframe e cria um gráfico de barras para a quantidade de prêmios dos álbuns mais premiados 
def albuns_awards_plot(dataframe):
    data = ae.albuns_awards(dataframe)
    plot = sns.barplot(data=data, x="Awards", y=data.index,color = 'g')
    plot.set(title='Mais longas')
    plt.show()

# Recebe um dataframe e cria um scatterplot que associa duração e popularidade 
def duration_popularity_plot(dataframe):
    plot = sns.scatterplot(data=dataframe, x="Duration", y="Popularity",color = 'g')
    plot.set(title='Duração x Popularidade')
    plt.show()

# Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nas letras 
def common_words_by_lyrics_plot(dataframe):
    resultado = ae.common_words_by_lyrics(dataframe)
    frequency = {}
    for tupla in resultado: 
        frequency[tupla[0]] = tupla[1]
    wc = WordCloud(background_color="black", max_words=1000)
    wc.generate_from_frequencies(frequency)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

# Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos das faixas     
def common_words_by_song_plot(dataframe):
    resultado = ae.common_words_by_song(dataframe)
    frequency = {}
    for tupla in resultado: 
        frequency[tupla[0]] = tupla[1]
    wc = WordCloud(background_color="black", max_words=1000)
    wc.generate_from_frequencies(frequency)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
 
# Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos dos álbuns    
def common_words_by_album_plot(dataframe):
    resultado = ae.common_words_by_album(dataframe)
    frequency = {}
    for tupla in resultado: 
        frequency[tupla[0]] = tupla[1]
    wc = WordCloud(background_color="black", max_words=1000)
    wc.generate_from_frequencies(frequency)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
