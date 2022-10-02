# Importa as bibliotecas necessárias 
import deezer
import pandas as pd
import time

# Recebe o nome de um artista ou banda e retorna seus dados extraídos da plataforma Deezer
def artist_info(searched_artist):
    client = deezer.Client() #Sincroniza com a plataforma 
    artist = client.search_artists(searched_artist)[0] #Retorna o primeiro resultado para o artista pesquisado
    artist_name = artist.name
    artist_nb_album = artist.nb_album
    artist_nb_fans = artist.nb_fan
    artist_albums = artist.get_albums()
    return artist_name, artist_nb_album, artist_nb_fans, artist_albums

# Recebe um álbum e retorna os seus gêneros em formato de string
def genres(album): 
    album_genres_list = []
    album_genres = album.genres
    for genre in album_genres:
        album_genres_list.append(genre.name) #Adiciona em uma lista os nomes dos gêneros
    album_genres_str = "/".join(album_genres_list) #Transforma a lista em uma string
    return album_genres_str
    
# Recebe um álbum e retorna seus dados extraídos da plataforma Deezer
def album_info(album):
    album_title = album.title
    album_genres = genres(album)
    album_nb_tracks = album.nb_tracks
    album_fans = album.fans
    album_release_date = album.release_date.strftime("%d/%m/%Y")
    album_tracks = album.tracks
    return album_title, album_genres, album_nb_tracks, album_fans, album_release_date, album_tracks
    
    
# Recebe uma faixa e retorna os seus contribuintes em formato de string
def contribuitors(track):
    track_contributors = track.contributors 
    track_contributors_list = []
    for contributor in track_contributors:
        track_contributors_list.append(contributor.name) #Adiciona em uma lista os nomes dos contribuintes
        track_contributors_str = "/".join(track_contributors_list)#Transforma a lista em uma string
    return track_contributors_str
    
# Recebe uma faixa e retorna a string "Yes" se ela for explícita e "No" se não for
def is_explicit(track):
    track_explicit_lyrics=track.explicit_lyrics
    if track_explicit_lyrics == True:
        track_explicit_lyrics_str = "Yes"
    else:
        track_explicit_lyrics_str = "No"
    return track_explicit_lyrics_str

# Recebe uma faixa e retorna os dados de cada uma extraídos da plataforma Deezer
def track_info(track):
    track_title = track.title
    track_duration = time.strftime("%M:%S", time.gmtime(track.duration))
    track_position = track.track_position
    track_disk_number = track.disk_number
    track_explicit_lyrics = is_explicit(track) #Utiliza a função de apoio is_explicit
    track_gain = track.gain
    track_contributors = contribuitors(track) #Utiliza a função de apoio contribuitors
    return track_title, track_duration, track_position, track_disk_number, track_explicit_lyrics, track_gain, track_contributors

#Utiliza as outras funções para criar um dataframe com informações da discografia do artista
def discography(artist):
    try:
        #Cria um dicionário onde serÃ£o armazenadas as informações sobre a discografia do artista
        song_data = {"Album": [], 
                     "Genre": [], 
                     "Release Date": [], 
                     "Track Name": [], 
                     "Track Number": [], 
                     "Artist Names": [], 
                     "Duration": [], 
                     "Explicit": [], 
                     "Gain": []}
        # albums = artist_info(artist)[3]# Busca os álbuns do artista
        artist_name, artist_nb_album, artist_nb_fans, artist_albums = artist_info(artist) # Busca os álbuns do artista
        for album in artist_albums:
            # album_data
            album_title, album_genres, album_nb_tracks, album_fans, album_release_date, album_tracks = album_info(album) #Busca a informação de cada album
            
            track_counter = 0
            
            # Busca as faixas em um álbum
            for track in album_tracks:
                track_title, track_duration, track_position, track_disk_number, track_explicit_lyrics, track_gain, track_contributors = track_info(track) #Busca a informação de cada faixa
                #Adiciona no dicionário song_data as informações de cada faixa
                
                track_counter += 1
                if track_disk_number > 1:
                    track_position = track_counter
                
                song_data.get("Album").append(album_title)
                song_data.get("Genre").append(album_genres)
                song_data.get("Release Date").append(album_release_date)
                song_data.get("Track Number").append(track_position)
                song_data.get("Track Name").append(track_title)
                song_data.get("Artist Names").append(track_contributors)
                song_data.get("Duration").append(track_duration)
                song_data.get("Explicit").append(track_explicit_lyrics)
                song_data.get("Gain").append(track_gain)
                df_discografia = pd.DataFrame.from_dict(song_data) # Cria um dataframe a partir do dicionário
    except TypeError as te: #Avisa ao usuário caso a função não receba uma string
        print("Essa função deve receber uma string;",te)
    except IndexError as ie: #Avisa ao usuário caso o artista procurado não seja encontrado
        print("Artista não encontrado;",ie)
    else:
        df_discografia.to_csv("discografia.csv", sep=";", encoding="utf-8-sig", index=False) #Converte o dataframe para um arquivo csv
        print("Arquivo criado com sucesso")

discography("Coldplay")
