# Visualização
''' Módulo de Visualização
    --------------------------------

Esse módulo contém funções responsáveis por gerar gráficos a partir da análise de dataframes sobre musicas em um formato específico.
O formato do dataframe deve ser igual ao gerado pelo módulo database nesse mesmo repositório e lido pela função create_dataframe no arquivo principal (main.py).

'''

# Importe as bibliotecas necessárias
import warnings
import exploratory_analysis as ae
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
from wordcloud import WordCloud

#Ignora avisos
warnings.filterwarnings("ignore")

# Use fundo preto para os gráficos
plt.style.use("dark_background")

# Adiciona alguns parâmetros com tamanho da figura e fonte da letra para todos os gráficos
plt.rcParams.update(
    {   'figure.figsize': (16,9),
        'font.family': 'stixgeneral',
    }
)

# Ajusta o padding dos gráficos
plt.tight_layout()


# Recebe um dataframe e cria um gráfico de barras para a popularidade das músicas mais ouvidas 
def most_listened_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a popularidade das músicas mais ouvidas.
    
    :param dataframe: DataFrame com coluna ``Popularity``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Gráfico de barras para a popularidade das músicas mais ouvidas em uma pasta separada.
    :rtype: `None`
    
    """
    data = ae.most_listened(dataframe)
    plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g') # Armazena um gráfico de barras
    plot.set(title='Mais ouvidas')
    plt.savefig('./images/most_listened.png')  #Salva o gráfico na pasta "images"
    plt.show()

# Recebe um dataframe e cria um gráfico de barras para a popularidade das músicas menos ouvidas       
def least_listened_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a popularidade das músicas menos ouvidas.
    
    :param dataframe: DataFrame com coluna ``Popularity``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Gráfico de barras para a popularidade das músicas menos ouvidas em uma pasta separada.
    :rtype: `None`
    
    """
    data = ae.least_listened(dataframe)
    plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g')# Armazena um gráfico de barras
    plot.set(title='Menos ouvidas')
    plt.savefig('./images/least_listened.png') #Salva o gráfico na pasta "images"
    plt.show()

# Recebe um dataframe e cria um gráfico de barras para a duração das músicas mais longas     
def longest_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a duração das músicas mais curtas.
    
    :param dataframe: DataFrame com coluna ``Duration Seconds``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Gráfico de barras para a duração das músicas mais curtas em uma pasta separada.
    :rtype: `None`
    
    """
    data = ae.longest(dataframe)
    plot = sns.barplot(data=data, x="Duration Seconds", y=data.index.get_level_values(1), color = 'g')# Armazena um gráfico de barras
    plot.set(title='Mais longas')
    plt.savefig('./images/longest.png')#Salva o gráfico na pasta "images"
    plt.show()

# Recebe um dataframe e cria um gráfico de barras para a duração das músicas mais curtas       
def shortest_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a duração das músicas mais curtas.
    
    :param dataframe: DataFrame com coluna ``Duration Seconds``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Gráfico de barras para a duração das músicas mais curtas em uma pasta separada.
    :rtype: `None`
    
    """
    data = ae.shortest(dataframe)
    plot = sns.barplot(data=data, x="Duration Seconds", y=data.index.get_level_values(1), color = 'g')# Armazena um gráfico de barras
    plot.set(title='Mais longas')
    plt.savefig('./images/shortest.png')#Salva o gráfico na pasta "images"
    plt.show()

# Recebe um dataframe e cria gráficos de barras para a popularidade das músicas mais ouvidas por álbum    
def most_listened_by_album_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a popularidade das músicas mais ouvidas por álbum.  
    
    :param dataframe: DataFrame com ``Album Name`` como parte do multi index e com a coluna ``Popularity``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Gráfico de barras para a popularidade das músicas mais ouvidas por álbum em uma pasta separada.
    :rtype: `None`
    
    """
    grouped = dataframe.groupby(level=0)
    for album, album_dataframe in grouped: #Itera para criar gráficos para cada álbum existente
        data = ae.most_listened(album_dataframe)
        plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g')# Armazena um gráfico de barras
        plot.set(title=f'Mais ouvidas em {album}')
        plt.savefig(f'./images/most_listened_{album}.png')#Salva o gráfico na pasta "images"
        plt.show()

# Recebe um dataframe e cria gráficos de barras para a popularidade das músicas menos ouvidas por álbum    
def least_listened_by_album_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a popularidade das músicas menos ouvidas por álbum.  
    
    :param dataframe: DataFrame com ``Album Name`` como parte do multi index e com a coluna ``Popularity``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Gráfico de barras para a popularidade das músicas menos ouvidas por álbum em uma pasta separada.
    :rtype: `None`
    
    """
    grouped = dataframe.groupby(level=0)
    for album, album_dataframe in grouped: #Itera para criar gráficos para cada álbum existente
        data = ae.least_listened(album_dataframe)
        plot = sns.barplot(data=data, x="Popularity", y=data.index.get_level_values(1), color = 'g')# Armazena um gráfico de barras
        plot.set(title=f'Menos ouvidas em {album}')
        plt.savefig(f'./images/least_listened_{album}.png')#Salva o gráfico na pasta "images"
        plt.show()
        
# Recebe um dataframe e cria gráficos de barras para a duração das músicas mais longas por álbum 
def longest_by_album_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a duração das músicas mais longas por álbum  
    
    :param dataframe: DataFrame com ``Album Name`` como parte do multi index e com a coluna ``Duration Seconds``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Gráfico de barras para a popularidade das músicas menos ouvidas por álbum em uma pasta separada.
    :rtype: `None`
    
    """
    grouped = dataframe.groupby(level=0)
    for album, album_dataframe in grouped: #Itera para criar gráficos para cada álbum existente
        data = ae.longest(album_dataframe)
        plot = sns.barplot(data=data, x="Duration Seconds", y=data.index.get_level_values(1), color = 'g')# Armazena um gráfico de barras
        plot.set(title=f'Mais longas em {album}')
        plt.savefig(f'./images/longest_{album}.png')#Salva o gráfico na pasta "images"
        plt.show()

# Recebe um dataframe e cria gráficos de barras para a duração das músicas mais longas por álbum 
def shortest_by_album_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a duração das músicas mais curtas por álbum.  
    
    :param dataframe: DataFrame com ``Album Name`` como parte do multi index e com a coluna ``Duration``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Gráfico de barras para a duração das músicas mais curtas por álbum em uma pasta separada.
    :rtype: `None`
    
    """
    grouped = dataframe.groupby(level=0)
    for album, album_dataframe in grouped:#Itera para criar gráficos para cada álbum existente
        data = ae.shortest(album_dataframe)
        plot = sns.barplot(data=data, x="Duration Seconds", y=data.index.get_level_values(1), color = 'g')# Armazena um gráfico de barras
        plot.set(title=f'Menos longas em {album}')
        plt.savefig(f'./images/shortest_{album}.png')#Salva o gráfico na pasta "images"
        plt.show()
        
# Recebe um dataframe e cria um gráfico de barras para a quantidade de prêmios dos álbuns mais premiados 
def albuns_awards_plot(dataframe):
    """Recebe um dataframe e cria e plota um gráfico de barras para a quantidade de prêmios dos álbuns mais premiados.
    
    :param dataframe: DataFrame com a coluna ``Awards``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Gráfico de barras para a quantidade de prêmios dos álbuns mais premiados em uma pasta separada
    :rtype: `None`
    
    """
    data = ae.albuns_awards(dataframe)
    plot = sns.barplot(data=data, x="Awards", y=data.index,color = 'g') # Armazena um gráfico de barras
    plot.set(title='Mais premiadas')
    plt.savefig('./images/awards.png')#Salva o gráfico na pasta "images"
    plt.show()

# Recebe um dataframe e cria um scatterplot que associa duração e popularidade 
def duration_popularity_plot(dataframe):
    """Recebe um dataframe e cria e plota um scatterplot que associa duração e popularidade.

    :param dataframe: DataFrame com com a coluna ``Duration Seconds`` e ``Popularity``
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Scatterplot que associa duração e popularidade em uma pasta separada.
    :rtype: `None`
    """
    plot = sns.scatterplot(data=dataframe, x="Duration Seconds", y="Popularity",color = 'g') # Armazena um gráfico de barras
    plot.set(title='Duração x Popularidade')
    plt.savefig('./images/duration_popularity.png')#Salva o gráfico na pasta "images"
    plt.show()

def common_words_by_lyrics_plot(dataframe):
    """Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nas músicas. 
    
    :param dataframe: DataFrame com a coluna ``Track Lyrics``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Nuvem de palavras com as palavras mais comuns nas músicas.
    :rtype: `None`
    
    """
    resultado = ae.common_words_by_lyrics(dataframe)
    frequency = {}
    for tupla in resultado: 
        frequency[tupla[0]] = tupla[1] #Cria um dicionário com as palavras e frequências
    wc = WordCloud(background_color="black", max_words=1000) #Cria nuvem de palavras
    wc.generate_from_frequencies(frequency)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('./images/common_words_by_lyrics.png')#Salva o gráfico na pasta "images"
    plt.show()

# Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos das faixas     
def common_words_by_song_plot(dataframe):
    """Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos das faixas. 
    
    :param dataframe: DataFrame com a coluna ``Track Name``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Nuvem de palavras com as palavras mais comuns nos títulos das faixas.
    :rtype: `None`
    
    """
    resultado = ae.common_words_by_song(dataframe)
    frequency = {}
    for tupla in resultado: 
        frequency[tupla[0]] = tupla[1]#Cria um dicionário com as palavras e frequências
    wc = WordCloud(background_color="black", max_words=1000)#Cria nuvem de palavras
    wc.generate_from_frequencies(frequency)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('./images/common_words_by_song.png')#Salva o gráfico na pasta "images"
    plt.show()
 
# Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos dos álbuns    
def common_words_by_album_plot(dataframe):
    """Recebe um dataframe e cria uma nuvem de palavras com as palavras mais comuns nos títulos dos álbuns.   
    
    :param dataframe: DataFrame com a coluna ``Album Name``.
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Nuvem de palavras com as palavras mais comuns nos títulos dos álbuns.
    :rtype: `None`
    
    """
    resultado = ae.common_words_by_album(dataframe)
    frequency = {}
    for tupla in resultado: #Cria um dicionário com as palavras e frequências
        frequency[tupla[0]] = tupla[1]
    wc = WordCloud(background_color="black", max_words=1000)#Cria nuvem de palavras
    wc.generate_from_frequencies(frequency)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('./images/common_words_by_album.png')#Salva o gráfico na pasta "images"
    plt.show()
