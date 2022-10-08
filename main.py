## Importe os módulos e bibliotecas necessárias

import sys
sys.path.insert(1, './analysis_module')

import dataframe_reader as reader
import exploratory_analysis as expan
import pandas as pd
import visualization as vis

# Crie o dataframe
dataframe = reader.is_valid("./COLDPLAY/artist_data.csv")
dataframe = reader.add_awards(dataframe,'./COLDPLAY/albuns_awards.csv')
dataframe = reader.create_final_dataframe(dataframe)

# Imprima os resultados da análise exploratória.
print("Músicas mais ouvidas por álbum: ")
print(expan.most_listened_by_album(dataframe))

print("#"*80,"\n")

print("Músicas menos ouvidas por álbum:")
print(expan.least_listened_by_album(dataframe))

print("#"*80,"\n")

print("Músicas mais longas por álbum:")
print(expan.longest_by_album(dataframe))

print("#"*80,"\n")

print("Músicas menos longas por álbum:")
print(expan.shortest_by_album(dataframe))

print("#"*80,"\n")

print("Músicas mais ouvidas: ")
print(expan.most_listened(dataframe))

print("#"*80,"\n")

print("Músicas menos ouvidas: ")
print(expan.least_listened(dataframe))

print("#"*80,"\n")

print("Músicas mais longas:")
print(expan.longest(dataframe))

print("#"*80,"\n")

print("Músicas menos longas:")
print(expan.shortest(dataframe))

print("#"*80,"\n")

print("Álbuns mais premiados:")
print(expan.albuns_awards(dataframe))

print("#"*80,"\n")

print("Correlação entre duração e popularidade:")
print(expan.duration_popularity(dataframe))

print("#"*80,"\n")

print("Palavras mais comuns nas letras e suas respectivas frequências:")
print(expan.common_words_by_lyrics(dataframe))

print("#"*80,"\n")

print("Palavras mais comuns nos títulos das faixas e suas respectivas frequências:")
print(expan.common_words_by_song(dataframe))

print("#"*80,"\n")

print("Palavras mais comuns nos títulos dos álbuns e suas respectivas frequências:")
print(expan.common_words_by_album(dataframe))

print("#"*80,"\n")

print("Palavras mais comuns nas letras das músicas em cada álbum:")
print(expan.common_words_lyrics_album(dataframe))

print("#"*80,"\n")

print("Palavras mais comuns entre o títulos dos álbuns e as letras das músicas: ")
print(expan.album_in_lyrics(dataframe))

print("#"*80,"\n")

print("Palavras mais comuns entre o títulos das faixas e as letras das músicas:")
print(expan.song_in_lyrics(dataframe))

print("#"*80,"\n")

print("Popularidade média entre as músicas explícitas e não explícitas")
print(expan.explicit_popularity(dataframe))

print("#"*80,"\n")

print("Álbuns mais populares")
print(expan.most_popular_album(dataframe))

print("#"*80,"\n")

print("Gêneros mais frequêntes na discografia")
print(expan.common_gender(dataframe))

vis.most_listened_plot(dataframe)
vis.least_listened_plot(dataframe)
vis.longest_plot(dataframe)
vis.shortest_plot(dataframe)

vis.most_listened_by_album_plot(dataframe)
vis.least_listened_by_album_plot(dataframe)
vis.longest_by_album_plot(dataframe)
vis.shortest_by_album_plot(dataframe)

vis.albuns_awards_plot(dataframe)
vis.duration_popularity_plot(dataframe)

vis.common_words_by_lyrics_plot(dataframe)
vis.common_words_by_song_plot(dataframe)
vis.common_words_by_album_plot(dataframe)
