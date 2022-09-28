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
