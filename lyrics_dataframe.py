import json
import re

import numpy as np
import pandas as pd

from lyricsgenius import Genius

# Armazena o token de acesso, obtido através da plataforma Genius
access_token = "u2SqMOrCtzWwY9xGxI6PiLn5aVqnhzWMiaMWB2BmrfuvJQL-Z_nQ4pv8gJej4isU"

# Instancia o objeto principal da API do Genius
genius = Genius(access_token, timeout=60, retries=10)

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

# Obtém o nome e o id do artista
artist_name, artist_id = get_artist_info("Coldplay")

# Obtém uma lista de álbuns, contendo seu nome e id do álbum
albums = get_albums_info(artist_id)