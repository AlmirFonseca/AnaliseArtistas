import os

import spotipy #pip install spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import time
import pandas as pd

### Possíveis erros de spotifyData.py ###
## Erros na função que irá para a main.py ##
## Erro de conexão:
#     -> Gerar print("Sem conexão à internet")
## Credenciais inválidas (client_id, client_secret):
#     -> Se as duas entradas forem incompatíveis/inválidas, erro! 
#     -> Gerar print("credenciais inválidas"), exceção gerada pela API
#     -> Se as credenciais são inválidas, nada será gerado, produzido, ou pesquisado
## Nome de artista inválido (artist):
#     -> Se o nome do artista for inválido, erro! 
#     -> Gerar print("nome de artista inválido")
#     -> Se o nome do artista é inválido, nada será gerado, produzido, ou pesquisado
## (get_singles, duplicate, save_csv,) são por default (False, False, False), caso sejam inválidos, será utilizada o default

# Define as credenciais para o uso da API
client_id = "6a1edef9875b4c79a81e70db08f91c79"
client_secret = "bd17a1c083284bd4882f1c0839a6df65"

# Função de Autenticação
def autentication(client_id, client_secret):
    if type(client_id) != str:
        raise Exception("ID deve ser uma string!")
    elif type(client_secret) != str:
        raise Exception("Secret deve ser uma string!")
    else:
        credentials = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
        return credentials

# Função que instancia o objeto principal da API
def spotify_object(client_credentials_manager):
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp

# Função que realiza uma pesquisa sobre id de um artista
def artist_id(sp, artist):
    if type(artist) != str:
        raise Exception("Artista deve ser uma string!")
    else:
        #Pesquisa na API por meio do nome do artista dado
        #Erros relacionados a credenciais inválidas são levantados pela própria spotipy
        artist = sp.search(artist, type="artist", limit=1)
        #Armazena o ID do artista
        try:
            artist_id = artist.get("artists").get("items")[0].get("id")
        except IndexError:
            raise Exception("Nome de artista inserido não encontrado")
        return artist_id

# Função que realiza uma pesquisa sobre nome oficial de um artista
def artist_name(sp, artist):
    if type(artist) != str:
        raise Exception("Artista deve ser uma string!")
    else:
        #Pesquisa na API por meio do nome do artista dado
        #Erros relacionados a credenciais inválidas são levantados pela própria spotipy
        artist_info = sp.search(artist, type="artist", limit=1)
        #Armazena o nome oficial do artista no Spotify
        try:
            artist_name = artist_info.get("artists").get("items")[0].get("name")
        except IndexError:
            raise Exception("Nome de artista inserido não encontrado")
        return artist_name

# Função que realiza coleta de dados sobre álbuns de artistas a partir
# do objeto principal da API, id do artista, e tipo de álbum ("single", "album")
def artist_albums_data(sp, artist_id, get_singles = False, duplicate = False):
    #get_singles -> True = Single and Album
    #get_singles -> False (default) = Album

    # Criação de dicionário para armazenamento  dos dados dos álbuns do artista
    albums_data = {}

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
            # Pesquisa na API por meio do id do artista dado
            # Erros relacionados a id inválido são levantados pela própria spotipy
            # Erros relacionados a credenciais inválidas são levantados pela própria spotipy
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
                album_dict = { 
                            "id" : album_id,
                            "name" : album_name,
                            "release_date" : album_release_date,
                            "num_tracks" : album_num_tracks}
                
                if duplicate != True:
                    # Verifica a existência de nome de álbum no dict gerado até o momento
                    if album_name in albums_data.keys():
                        # Caso exista, é acessado o nome do dicionário já existente (old) e o novo, e a quantidade
                        # de tracks
                        num_tracks_album_old = albums_data.get(album_name).get("num_tracks")
                        num_tracks_album_new = album_num_tracks
                        #Caso a quantidade de tracks do novo seja maior que o antigo é sobreescrito pelo novo
                        if num_tracks_album_new > num_tracks_album_old:
                            albums_data[album_name] = album_dict
                        else:
                        #Caso não seja, é ignorado e descartado
                            pass
                    else:
                        #Caso não exista, é adicionado ao dicionário
                        albums_data[album_name] = album_dict
                else:
                    # Acumula os dicionários no dicionário criado
                    albums_data[album_name] = album_dict
            # Checa se ainda há mais álbuns a serem buscados
            if albums_response.get("next") == None:
                break
            i += 50
    #Acessa os valores do dicionário e converte em uma lista
    albums_data = list(albums_data.values())
    return albums_data

def track_is_explicit(track):
    #Como o track_id_explicit recebe um booleano, podemos convertê-lo para uma string 
    # de "Yes" ou "No"
    track_id_explicit = track.get("explicit")
    if track_id_explicit == True:
        track_id_explicit = "Yes"
    else:
        track_id_explicit = "No"
    return track_id_explicit

def track_duration_s(track):
    #Conversão da duração dada em ms para seg
    track_duration_ms = track.get("duration_ms")
    track_duration_s = track_duration_ms / 1000
    #Conversão da duração modificada em seg para formato mm:ss
    track_duration_formatted = time.strftime("%M:%S", time.gmtime(track_duration_s))
    return track_duration_formatted

def track_feature_mode(track_audio_features):
    #Como "mode" retorna 0 ou 1, equivalentes a "minor" e "major", podemos convertê-lo para uma string 
    mode = track_audio_features.get("mode")
    if mode == "0":
        mode = "Minor"
    elif mode == "1":
        mode =  "Major"
    else:
        mode =  " "
    return mode

def track_feature_key(track_audio_features):
    #Como "key" retorna 0, para "C", 1 para "C♯/D♭", assim em diante, podemos convertê-lo para uma string do tom correspondente 
    key = track_audio_features.get("key")
    if key == 0:
        key = "C"
    elif key == 1:
        key = "C♯/D♭"
    elif key == 2:
        key = "D"
    elif key == 3:
        key = "D♯/E♭"
    elif key == 4:
        key = "E"
    elif key == 5:
        key = "F"
    elif key == 6:
        key = "F♯/G♭"
    elif key == 7:
        key = "G"
    elif key == 8:
        key = "G♯/A♭"
    elif key == 9:
        key = "A"
    elif key == 10:
        key = "A♯/B♭"
    elif key == 11:
        key = "B"
    else:
        key = " "
    return key

def track_feature_timesig(track_audio_features):
    #Como "timesig" retorna um número de 3 a 7, equivalentes a 3/4 até 7/4,
    #podemos convertê-lo para uma string do tempo correspondente
    timesig = track_audio_features.get("time_signature")
    timesig = f'{timesig}/4'
    return timesig

# Função que coleta os dados de cada faixa de cada álbum
def artist_albums_track_data(sp, albums_data):
    # Inicia um contador para armazenar e exibir o número de faixas processadas
    track_counter = 0

    # Criação de lista para armazenamento  dos dados das faixas do artista de cada álbum
    tracks_data = list()    

    if type(albums_data) != list:
        raise Exception("albums_data aceita apenas listas")

    # Itera sobre cada álbum presente no albums_data (o próprio dict criado na função "artist_albums_data")
    for album in albums_data:
        print("\n", "=-"*30, "\n", sep="")
        print("Analisando álbum:", album.get("name"))
        
        # Recolhe o id de cada álbum
        try:
            album_id = album.get("id")
            if type(album_id) == None:
                raise Exception("Dicionário sem ids")
        except AttributeError:
            raise Exception("A lista não contém dicionários no formato especificado")

        # Inicia uma lista vazia, que armazenará os IDs das faixas de cada álbum
        tracks_ids = list()
        
        # Cria um loop para obter da API os dados das faixas de cada álbum
        i = 0
        while True:
            # Erros relacionados a credenciais inválidas são levantados pela própria spotipy
            # Recebe os dados em blocos de 50 faixas
            # Armazena cada faixa por álbum
            try: 
                tracks = sp.album_tracks(album_id, limit=50, offset=i)
            except AttributeError:
                raise Exception("Ids inválidos")
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

            # Contador da quantidade de tracks já iterada por álbum resetado a cada álbum
            track_count_album = 1

            for track in tracks_list:
                track_id = track.get("id")
                
                tracks_ids.append(track_id)
                
                track_name = track.get("name")
                track_popularity = track.get("popularity")
                
                #Chamamos função de apoio is_explicit() para conversão
                track_id_explicit = track_is_explicit(track)
                
                #Chamamos função de apoio duration() para conversão
                track_duration = track_duration_s(track)
                                
                track_disc_number = track.get("disc_number")
                track_number = track_count_album
                
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
                #Chamamos função de poio track_feature_key() para conversão
                track_key = track_feature_key(track_audio_features)
                #Chamamos função de apoio track_feature_mode() para conversão
                track_mode = track_feature_mode(track_audio_features)
                #Chamamos função de apoio track_feature_timesig() para conversão
                track_time_signature = track_feature_timesig(track_audio_features)
                track_danceability = track_audio_features.get("danceability")
                track_energy = track_audio_features.get("energy")
                track_speechiness = track_audio_features.get("speechiness")
                track_acousticness = track_audio_features.get("acousticness")
                track_instrumentalness = track_audio_features.get("instrumentalness")
                track_liveness = track_audio_features.get("liveness")
                track_valence = track_audio_features.get("valence")

                # Armazena os dados num dicionário
                track_dict = {"Album ID": album.get("id"),
                              "Album Name": album.get("name"),
                              "Release Date": album.get("release_date"),
                              "Track Name" : track_name,
                              "Disc Number": track_disc_number,
                              "Track Number" : track_number,
                              "Artist Names" : track_artists_names,
                              "Popularity" : track_popularity,
                              "Explicit" : track_id_explicit, 
                              "Duration" : track_duration,
                              "Loudness" : track_loudness,
                              "Tempo" : track_tempo,
                              "Key" : track_key,
                              "Mode" : track_mode,
                              "Time Signature" : track_time_signature,
                              "Danceability" : track_danceability,
                              "Energy" : track_energy,
                              "Speechiness" : track_speechiness,
                              "Acousticness" : track_acousticness,
                              "Instrumentalness" : track_instrumentalness,
                              "Liveness" : track_liveness,
                              "Valence" : track_valence
                              }
            
                # Acumula os dicionários na lista criada
                tracks_data.append(track_dict)
                
                # Imprime, no console, o número de músicas já processadas e o número da faixa  dentro do álbum
                track_counter += 1
                print("Faixa: ", track_count_album, " Nº de músicas: ", track_counter, "\n", sep="")

                track_count_album +=1
            # Checa se ainda há mais álbuns a serem buscados    
            if tracks.get("next") == None:
                break
            i += 50

    return tracks_data

# Gera um dataframe a partir dos dados coletados, com a opção de salvar o dataframe num arquivo ".csv"
def generate_dataframe(artist_name, tracks_data, save_csv = False):
    # Obtém o nome das colunas do dataframe a partir dos dados que cada faixa possui
    dataframe_columns = list(tracks_data[0].keys())

    # Inicializa uma lista para acumular os dados de cada faixa
    track_list = []
    
    # Itera sobre cada faixa, coletando seus dados e acumulando na lista criada
    for track in tracks_data:
        track_list.append(list(track.values()))
        
    # Gera um pandas DataFrame a partir dos dados coletados
    tracks_dataframe = pd.DataFrame(data=track_list, columns=dataframe_columns)
    
    # Caso o usuário deseje salvar o dataframe num arquivo ".csv"
    if save_csv:
        # Gera um caminho relativo, com o nome do artista
        csv_path = f"Dados das faixas - {artist_name}.csv"
        
        # Salva o dataframe num arquivo ".csv"
        tracks_dataframe.to_csv(csv_path, sep=";", encoding="utf-8-sig", index=False)
        # Exibe uma mensagem de sucesso e exibe o local do arquivo gerado
        print("O arquivo CSV foi gerado e salvo em:\n", os.path.abspath(csv_path), sep="")

    # A função retorna o dataframe gerado
    return tracks_dataframe

def get_spotify_data(client_id, client_secret, artist, get_singles = False, duplicate = False, save_csv = False):
    client_credentials_manager = autentication(client_id, client_secret)
    sp = spotify_object(client_credentials_manager)
    name = artist_name(sp, artist)
    id = artist_id(sp, name)
    albums_data = artist_albums_data(sp, id, get_singles, duplicate)
    track_data = artist_albums_track_data(sp, albums_data)
    df = generate_dataframe(name, track_data, save_csv)
    return  df

print(get_spotify_data(client_id, client_secret, "coldplay", get_singles = True, duplicate =  False, save_csv = True))
