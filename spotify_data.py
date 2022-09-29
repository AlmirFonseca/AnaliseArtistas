import spotipy #pip install spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import time
import pandas as pd

# Define as credenciais para o uso da API
# client_id = "6a1edef9875b4c79a81e70db08f91c79"
# client_secret = "bd17a1c083284bd4882f1c0839a6df65"

# Função de Autenticação
def autentication(client_id, client_secret):
    credentials = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
    return credentials

# Função que instancia o objeto principal da API
def spotify_object(client_credentials_manager):
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp

# Função que realiza uma pesquisa sobre id de um artista
def artist_id(sp, artist):
    if type(artist) != str:
        raise Exception("Não foi inserido uma entrada de artista válida")
    else:
        #Pesquisa na API por meio do nome do artista dado
        artist = sp.search(artist, type="artist", limit=1)
        #Armazena o ID do artista
        artist_id = artist.get("artists").get("items")[0].get("id")
        return artist_id

# Função que realiza uma pesquisa sobre nome oficial de um artista
def artist_name(sp, artist):
    #Pesquisa na API por meio do nome do artista dado
    artist_info = sp.search(artist, type="artist", limit=1)
    #Armazena o nome oficial do artista no Spotify
    artist_name = artist_info.get("artists").get("items")[0].get("name")
    return artist_name

# Função que realiza coleta de dados sobre álbuns de artistas a partir
# do objeto principal da API, id do artista, e tipo de álbum ("single", "album")
def artist_albums_data(sp, artist_id, get_singles = False):
    #get_singles -> True = Single and Album
    #get_singles -> False (default) = Album

    # Criação de lista para armazenamento  dos dados dos álbuns do artista
    albums_data = list()

    #Verificação se foi optado somente pelos Albums ou se Albums e Singles
    if get_singles == True:
        album_types =  ["Album", "Single"]
    else:
        album_types = ["Album"]

    # Criação de contador de quantidade de buscas realizadas
    # OBS: Realiza buscas em blocos de 50 resultados (limite máximo da API)
    i = 0

    for type in album_types:
        while True:
            # Recebe a resposta da busca através da API
            albums_response = sp.artist_albums(artist_id, limit=50, offset=i, album_type = type)
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

# Função que coleta os dados de cada faixa de cada álbum
def artist_albums_track_data(sp, albums_data):
    # Inicia um contador para armazenar e exibir o número de faixas processadas
    track_counter = 0

    # Criação de lista para armazenamento  dos dados das faixas do artista de cada álbum
    tracks_data = list()    

    # Itera sobre cada álbum presente no albums_data (o próprio dict criado na função "artist_albums_data")
    for album in albums_data:

        # Recolhe o id de cada álbum
        album_id = album.get("id")

        # Inicia uma lista vazia, que armazenará os IDs das faixas de cada álbum
        tracks_ids = list()
        
        # Cria um loop para obter da API os dados das faixas de cada álbum
        i = 0
        while True:
        
            # Recebe os dados em blocos de 50 faixas
            # Armazena cada faixa por álbum 
            tracks = sp.album_tracks(album_id, limit=50, offset=i)
            # Armazena uma lista de faixas por álbum
            tracks_list = tracks.get("items")
            
            # Adiciona o ID de cada faixa à lista
            for track in tracks_list:
                track_id = track.get("id")
                tracks_ids.append(track_id)
            
            ## COMO ALBUM_TRACKS NÃO RETORNA DADOS SOBRE AS FAIXAS EM SI, 
            ## SERÁ NECESSÁRIO UTILIZAR O MÉTODO TRACKS, QUE OPERA SOBRE UMA LISTA DE IDS

            # Através da lista e do método tracks(), recolhemos informações de todas as faixas
            tracks = sp.tracks(tracks_ids)
            
            # Acessa a lista de resultados, onde cada dict é sobre uma faixa
            tracks_list = tracks.get("tracks")
            
            # Itera sobre cada faixa, recolhendo os seus principais atributos
            for track in tracks_list:
                track_id = track.get("id")
                
                tracks_ids.append(track_id)
                
                track_name = track.get("name")
                track_popularity = track.get("popularity")
                track_id_explicit = track.get("explicit")
                
                #Como o track_id_explicit recebe um booleano, podemos convertê-lo para uma string 
                # de "Yes" ou "No"
                if track_id_explicit == True:
                    track_id_explicit = "Yes"
                else:
                    track_id_explicit = "No"

                track_duration_ms = track.get("duration_ms")
                #Conversão da duração dada em ms para seg
                track_duration_s = track_duration_ms / 1000
                #Conversão da duração modificada em seg para formato mm:ss
                track_duration_formatted = time.strftime("%M:%S", time.gmtime(track_duration_s))
                
                track_disc_number = track.get("disc_number")
                track_number = track.get("track_number")
                
                track_artists_list = track.get("artists")
                #Criação de lista para armazenamento de nomes dos artistas 
                #(Considerando que há faixas com participações especiais)
                track_artists_names = list()

                #Itera sobre cada artista e forma uma lista de nomes dos artistas
                for artist in track_artists_list:
                    track_artists_names.append(artist.get("name"))

                #Junção de todos os artistas na lista e separação por "/"
                track_artists_names = "/".join(track_artists_names)
                
                #Acesso aos dados das faixas pelo id de cada faixa
                track_audio_features = sp.audio_features(track_id)[0]
                

                track_loudness = track_audio_features.get("loudness")
                track_tempo = track_audio_features.get("tempo")
                track_key = track_audio_features.get("key")
                track_mode = track_audio_features.get("mode")
                track_time_signature = track_audio_features.get("time_signature")
                track_danceability = track_audio_features.get("danceability")
                track_energy = track_audio_features.get("energy")
                track_speechiness = track_audio_features.get("speechiness")
                track_acousticness = track_audio_features.get("acousticness")
                track_instrumentalness = track_audio_features.get("instrumentalness")
                track_liveness = track_audio_features.get("liveness")
                track_valence = track_audio_features.get("valence")

                # Armazena os dados num dicionário
                track_dict = {"album_name": album.get("name"),
                              "album_date": album.get("release_date"),
                              "name" : track_name,
                              "disc_number" : track_disc_number,
                              "number" : track_number,
                              "artist_names" : track_artists_names,
                              "popularity" : track_popularity,
                              "explicit" : track_id_explicit, 
                              "duration" : track_duration_formatted,
                              "loudness" : track_loudness,
                              "tempo" : track_tempo,
                              "key" : track_key,
                              "mode" : track_mode,
                              "time_signature" : track_time_signature,
                              "danceability" : track_danceability,
                              "energy" : track_energy,
                              "speechiness" : track_speechiness,
                              "acousticness" : track_acousticness,
                              "instrumentalness" : track_instrumentalness,
                              "liveness" : track_liveness,
                              "valence" : track_valence
                              }
            
                # Acumula os dicionários na lista criada
                tracks_data.append(track_dict)
                
                # Imprime, no console, o número de músicas já processadas
                track_counter += 1
                print(track_counter)

            # Checa se ainda há mais álbuns a serem buscados    
            if tracks.get("next") == None:
                break
            i += 50
    return tracks_data

def get_spotify_data(client_id, client_secret, artist, get_singles = False):
    client_credentials_manager = autentication(client_id, client_secret)
    sp = spotify_object(client_credentials_manager)
    name = artist_name(sp, artist)
    id = artist_id(sp, name)
    albums_data = artist_albums_data(sp, id, get_singles)
    track_data = artist_albums_track_data(sp, albums_data)

    df = pd.DataFrame(track_data)

    return df
    
