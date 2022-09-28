import spotipy #pip install spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import time

# Define as credenciais para o uso da API
# client_id = "6a1edef9875b4c79a81e70db08f91c79"
# client_secret = "bd17a1c083284bd4882f1c0839a6df65"

# Função de Autenticação
def autentication(client_id, client_secret):
    credentials = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
    return credentials

#client_credentials_manager = autentication(client_id, client_secret)
#print(client_credentials_manager)

# Função que instancia o objeto principal da API
def spotify_object(client_credentials_manager):
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp

#sp = spotify_object(client_credentials_manager)
#print(sp)

# Função que realiza uma pesquisa sobre id de um artista
def artist_id(sp, artist):
    #Pesquisa na API por meio do nome do artista dado
    artist = sp.search(artist, type="artist", limit=1)
    #Armazena o ID do artista
    artist_id = artist.get("artists").get("items")[0].get("id")
    return artist_id

#id = artist_id(sp, "coldplay")
#print(id)

# Função que realiza uma pesquisa sobre nome oficial de um artista
def artist_name(sp, artist):
    #Pesquisa na API por meio do nome do artista dado
    artist_info = sp.search(artist, type="artist", limit=1)
    #Armazena o nome oficial do artista no Spotify
    artist_name = artist_info.get("artists").get("items")[0].get("name")
    return artist_name

#name = artist_name(sp, "coldplay")
#print(name)

# Função que realiza coleta de dados sobre álbuns de artistas a partir
# do objeto principal da API, id do artista, e tipo de álbum ("single", "album")
def artist_albums_data(sp, artist_id, album_type):
    # Criação de lista para armazenamento  dos dados dos álbuns do artista
    albums_data = list()

    # Criação de contador de quantidade de buscas realizadas
    # OBS: Realiza buscas em blocos de 50 resultados (limite máximo da API)
    i = 0
    while True:
        # Recebe a resposta da busca através da API
        albums_response = sp.artist_albums(artist_id, limit=50, offset=i, album_type = album_type)
        # Acessa a lista de álbuns
        albums_list = albums_response.get("items")
            
        # Itera sobre cada álbum
        for album in albums_list:
            
            # Recolhe os principais dados de cada álbum
            album_id = album.get("id")
            album_name = album.get("name")
            album_release_date = album.get("release_date")
            album_num_tracks = album.get("total_tracks")
            
            # Armazena os dados num dicionário
            album_dict = {"id" : album_id,
                        "name" : album_name,
                        "release_date" : album_release_date,
                        "num_tracks" : album_num_tracks}
            
            # Acumula os dicionários na lista criada
            albums_data.append(album_dict)
        
        # Checa se ainda há mais álbuns a serem buscados
        if albums_response.get("next") == None:
            break
        i += 50
    return albums_data

#albums_data_single = artist_albums_data(sp, id, "single")
#albums_data_album = artist_albums_data(sp, id, "album")
#print(albums_data_single, "\n", sep = "")
#print(albums_data_album, "\n", sep = "")
