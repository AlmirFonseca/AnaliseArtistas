# Análise exploratória

#Importe as bibliotecas necessárias
import pandas as pd
import numpy as np
import collections

# Imprime as 3 músicas mais ouvidas por álbum
def mais_ouvidas_album(dataframe):
    print(dataframe.groupby('Álbum')['Popularidade'].nlargest(3,keep='all'))
 
# Imprime as 3 músicas menos ouvidas por álbum   
def menos_ouvidas_album(dataframe):
    print(dataframe.groupby('Álbum')['Popularidade'].nsmallest(3,keep='all'))
    
# Imprime as 3 músicas mais longas por álbum
def mais_longas_album(dataframe):
    print(dataframe.groupby('Plataforma')['Duração'].nlargest(3,keep='all'))
    
# Imprime as 3 músicas menos longas por álbum
def menos_longas_album(dataframe):
    print(dataframe.groupby('Plataforma')['Duração'].nsmallest(3,keep='all'))
   
# Imprime as 3 músicas mais ouvidas na história do artista
def mais_ouvidas(dataframe):
    print(dataframe.nlargest(3, 'Popularidade',keep='all'))

# Imprime as 3 músicas menos ouvidas na história do artista
def menos_ouvidas(dataframe):
    print(dataframe.nsmallest(3, 'Popularidade',keep='all'))

# Imprime as 3 músicas mais longas na história do artista
def mais_longas(dataframe):
    print(dataframe.nlargest(3, 'Duração',keep='all'))
    
# Imprime as 3 músicas menos longas na história do artista
def menos_longas(dataframe):
    print(dataframe.nsmallest(3, 'Duração',keep='all'))
 
# Imprime a correlação de Pearson entre Duração e Popularidade
def duracao_popularidade(dataframe):
    correlacao = dataframe.corr(method ='pearson')
    print(correlacao.loc["Duração","Popularidade"])
    
# Imprime as 3 palavras mais comuns nos títulos dos álbuns
def palavra_comuns_album(dataframe):
    albuns = dataframe.index.get_level_values(0)
    lista_albuns = list(dict.fromkeys(albuns))
    lista_palavras = []
    for album in lista_albuns:
        palavras = album.split()
        for palavra in palavras:
            lista_palavras.append(palavra) 
    contador = collections.Counter(lista_palavras)
    mais_comuns = contador.most_common(3)
    print(mais_comuns)
    
    
# Imprime as 3 palavras mais comuns nos títulos das músicas
def palavra_comuns_titulo(dataframe):
    musicas = dataframe.index.get_level_values(1)
    lista_musicas = list(dict.fromkeys(musicas))
    lista_palavras = []
    for musica in lista_musicas:
        palavras = musica.split()
        for palavra in palavras:
            lista_palavras.append(palavra) 
    contador = collections.Counter(lista_palavras)
    mais_comuns = contador.most_common(3)
    print(mais_comuns)
    
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

    
