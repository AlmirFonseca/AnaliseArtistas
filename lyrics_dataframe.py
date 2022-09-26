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

# Obtém o nome e o id do artista
artist_name, artist_id = get_artist_info("Coldplay")