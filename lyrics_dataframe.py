import json
import re

import lyricsgenius
import numpy as np
import pandas as pd

# Armazena o token de acesso, obtido através da plataforma Genius
access_token = "u2SqMOrCtzWwY9xGxI6PiLn5aVqnhzWMiaMWB2BmrfuvJQL-Z_nQ4pv8gJej4isU"

# Instancia o objeto principal da API do Genius
genius = lyricsgenius.Genius(access_token, timeout=60, retries=10)

# Extrai os dados do artista através do seu nome
def get_artist_info(artist_name):
    # Realiza uma busca pelo nome do artista
    artist = genius.search_artist(artist_name, max_songs=0, get_full_info=False)
    
    # Retorna o nome e o id do artista na plataforma Genius
    return artist.name, artist.id

# Extrai os dados dos álbums através do id do artista
def get_albums_info(artist_id):
    # Inicializa uma lista para armazenar os dados de cada álbum
    albums_list = []
    
    # Busca por álbuns até que a API informe que não há mais páginas de resultados a serem exibidas
    next_page = 1
    while next_page != None:
        # Recebe o resultado da busca pelos álbuns de um artista
        album_response = genius.artist_albums(artist_id, page=next_page)
        
        print(album_response)
        
        # Verifica se existe mais alguma página de resultados a ser buscada
        next_page = album_response.get("next_page")
        
        # Itera sobre cada álbum
        for album in album_response.get("albums"):
            # Extrai o nome e id do álbum
            album_name = album.get("name")
            album_id = album.get("id")
            
            # Armazena esses dados num dicionario
            album_dict = {"id": album_id,
                          "name": album_name}
            
            # Adiciona o dicionário gerado à lista de álbuns
            albums_list.append(album_dict)
            
    # Retorna a lista de álbums gerada
    return albums_list

# Extrai os dados de cada faixa através do id do álbum
def get_album_tracks(albums):
    # Inicializa um contador de faixas processadas
    track_counter = 0
    
    # Inicializa uma lista para armazenar as faixas
    tracks = []
    
    # Itera sobre cada álbum
    for album in albums:
        # Coleta a lista de faixas de cada álbum a partir de seu id
        album_tracks = genius.album_tracks(album.get("id"))
        
        # Itera sobre cada faixa do album
        for track in album_tracks.get("tracks"):
            # Extrai o número da faixa
            track_number = track.get("number")
            
            # Acessa os metadados da faixa
            track_data = track.get("song")
            
            # Extrai o nome, id e data de lançamento da faixa
            track_name = track_data.get("title")
            track_id = track_data.get("id")
            track_release_date_components = track_data.get("release_date_components")
            
            try:
                # Converte o dicionário que contém os componentes da data para um datetime
                track_release_date = lyricsgenius.utils.convert_to_datetime(track_release_date_components).date()
            
            # Caso ocorra algum erro durante a conversão ou a API não disponibilize a data de lançamento da faixa
            except Exception as e:
                track_release_date = None
                print("Ocorreu um erro inesperado:", e)
            
            try:
                # Tenta obter a letra da música
                track_dict = genius.search_song(song_id=track_id, get_full_info=False)
                track_lyrics = track_dict.lyrics
                
            # Caso ocorra alguma exceção, consideraremos que nenhuma letra foi encontrada para a música
            except AttributeError:
                track_lyrics = ""
            
            except Exception as e:
                print("Ocorreu um erro inesperado:", e)
                track_lyrics = ""
                
            # Armazena os dados coletados num dicionário
            track_dict = {"album_name": album.get("name"),
                           "track_number": track_number,
                           "track_name": track_name,
                           "track_release_date": track_release_date,
                           "track_lyrics": track_lyrics}
            
            # Adiciona o dicionário gerado à lista de faixas
            tracks.append(track_dict)
            
            # Incrementa e exibe o contador e o nome da faixa processada
            track_counter += 1
            print(track_counter, track_name)
            
            # DEBUG: acelera o processo de debug, permitindo a análise de uma música por álbum
            # print(tracks)
            break
            
    # A função retorna uma lista de dicionários, onde cada dicionário contém os dados que descrevem cada faixa
    return tracks

# Obtém o nome e o id do artista
artist_name, artist_id = get_artist_info("Coldplay")

# Obtém uma lista de álbuns, contendo seu nome e id do álbum
albums = get_albums_info(artist_id)

# Obtém uma lista de faixas, contendo seu álbum, seu número, seu nome, sua data de lançamento e sua letra
tracks = get_album_tracks(albums)

print(tracks)