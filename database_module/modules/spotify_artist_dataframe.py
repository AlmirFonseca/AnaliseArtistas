# Spotify Data
''' Módulo de dados do Spotify
    ----------------------------

Esse módulo contém funções responsáveis por gerar um dataframe a partir dos dados da plataforma Spotify.

'''

import os

import spotipy 
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

# Função de Autenticação
def autentication(client_id, client_secret):
    """
    Recebe um client ID e um cliente secret para realizar autenticação e retornar credenciais.

    :param client_id: Cadeia de caracteres alfa-numérica única para cada cliente gerada pela plataforma Spotify representando seu ID.
    :type client_id: `str`
    :param client_secret: Cadeia de caracteres alfa-numérica única para cada cliente gerada pela plataforma Spotify representando seu secret.
    :type client_secret: `str`
    :return: Retorna um objeto de credenciais
    :rtype: `<class 'spotipy.oauth2.SpotifyClientCredentials'>`

    .. warning:: Client IDs e Client secrets são gerados pela plataforma Spotify e tem validade de duração!
    """
    if type(client_id) != str:
        raise TypeError("ID deve ser uma string!")
    elif type(client_secret) != str:
        raise TypeError("Secret deve ser uma string!")
    else:
        credentials = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
        return credentials

# Função que instancia o objeto principal da API
def spotify_object(client_credentials_manager):
    """
    Recebe um token de credenciais para criar e retornar o principal objeto da API do spotify.

    :param client_credentials_manager: Credenciais geradas a partir da função `spotifyData.autentication`
    :type client_credentials_manager: `<class 'spotipy.oauth2.SpotifyClientCredentials'>`
    :return: Retorna principal objeto da API do Spotify
    :rtype: `<class 'spotipy.client.Spotify'>`
    """
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp

# Função que realiza uma pesquisa sobre id de um artista
def get_artist_id(sp, artist):
    """
    Pesquisa pelo ID do artista dentro da plataforma Spotify

    :param sp: Objeto principal da API 
    :type sp: `<class 'spotipy.client.Spotify'>`
    :param artist: Artista escolhido 
    :type artist: `str`
    :raises Exception: _description_
    :raises Exception: _description_
    :return: Retorna o ID do artista dentro da plataforma Spotify
    :rtype: `str`
    """
    if type(artist) != str:
        raise Exception("Artista deve ser uma string!")
    else:
        #Pesquisa na API por meio do nome do artista dado
        #Erros relacionados a credenciais inválidas são levantados pela própria spotipy
        try:
            artist = sp.search(artist, type="artist", limit=1)
        except ConnectionError as error:
            print("Houve um problema na conexao")
            raise error
        except Exception as error:
            print("Houve um problema durante a execucao do projeto")
            raise error
        #Armazena o ID do artista
        try:
            artist_id = artist.get("artists").get("items")[0].get("id")
        except IndexError:
            raise Exception("Nome de artista inserido não encontrado")
        except Exception as error:
            print("Houve um problema durante a execucao do projeto")
            raise error
        return artist_id

# Função que realiza uma pesquisa sobre nome oficial de um artista
def get_artist_name(sp, artist):
    """
    Pesquisa pelo nome do artista dentro da plataforma Spotify

    :param sp: Objeto principal da API 
    :type sp: `<class 'spotipy.client.Spotify'>`
    :param artist: Artista escolhido 
    :type artist: `str`
    :raises Exception: _description_
    :raises Exception: _description_
    :return: Retorna o nome do artista dentro da plataforma Spotify
    :rtype: `str`
    """
    
    #Pesquisa na API por meio do nome do artista dado
    #Erros relacionados a credenciais inválidas são levantados pela própria spotipy
    
    try:
        artist_info = sp.search(artist, type="artist", limit=1)
    except ConnectionError as error:
        print("Houve um problema de conexao")
        raise error
    except Exception as error:
        print("Houve um problema durante a execucao do projeto")
        raise error
    
    #Armazena o nome oficial do artista no Spotify
    try:
        artist_name = artist_info.get("artists").get("items")[0].get("name")
    except IndexError:
        raise Exception("Nome de artista inserido não encontrado")
    return artist_name

# Função que realiza coleta de dados sobre álbuns de artistas a partir
# do objeto principal da API, id do artista, e tipo de álbum ("single", "album")
def artist_albums_data(sp, artist_id, get_singles = False, duplicate = False):
    """
    Pesquisa dentro da plataforma Spotify por todos os álbuns relacionados ao ID do artista dado e retorna uma lista de dicionários

    :param sp: Objeto principal da API 
    :type sp: `<class 'spotipy.client.Spotify'>`
    :param artist_id: ID do artista 
    :type artist_id: `str`
    :param get_singles: Valor booleano opcional que caso seja ``True``, será pesquisado informações sobre álbuns single, padrão como ``False``.
    :type get_singles: `bool`, opcional
    :param duplicate: Valor booleano opcional que caso seja ``True``, não será desconsiderado duplicatas de álbuns, padrão como ``False``.
    :type duplicate: `bool`, opcional
    :return: Lista de dicionários contendo informações sobre os álbuns
    :rtype: `list[dict]`

    .. warning:: Lista de dicionários de álbuns gerados pela função com parâmetro ``True`` não são suportados nessa versão!

    """

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

    for type_album in album_types:
        while True:
            # Recebe a resposta da busca através da API
            # Pesquisa na API por meio do id do artista dado
            # Erros relacionados a id inválido são levantados pela própria spotipy
            # Erros relacionados a credenciais inválidas são levantados pela própria spotipy
            
            try:
                albums_response = sp.artist_albums(artist_id, limit=50, offset=i, album_type = type_album)
            except ConnectionError as error:
                print("Houve um problema de conexao")
                raise error
            except Exception as error:
                print("Houve um problema durante a execucao do projeto")
                raise error
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
                
                if not duplicate:
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
    """
    Função de apoio para conversão de valores de ``is_explicit``. ``False`` para ``No``, e ``True`` para ``Yes`` 

    :param track: Dicionário com chave ``explicit`` contendo valores ``bool``
    :type track: `dict{bool}`
    :return: Converte ``False`` para ``No``, e ``True`` para ``Yes``
    :rtype: `str`
    """
    #Como o track_id_explicit recebe um booleano, podemos convertê-lo para uma string 
    # de "Yes" ou "No"
    track_id_explicit = track.get("explicit")
    if track_id_explicit == True:
        track_id_explicit = "Yes"
    else:
        track_id_explicit = "No"
    return track_id_explicit

def track_duration_s(track):
    """
    Função de apoio para conversão de valores de ``duration_ms``. Valores dados em milisegundos para segundos.

    :param track: Dicionário com chave ``duration_ms`` contendo valores dados em segundos.
    :type track: `dict{str}`
    :return: Valores dados em milisegundos para segundos.
    :rtype: `str`
    """
    #Conversão da duração dada em ms para seg
    track_duration_ms = track.get("duration_ms")
    track_duration_s = track_duration_ms / 1000
    #Conversão da duração modificada em seg para formato mm:ss
    track_duration_formatted = time.strftime("%M:%S", time.gmtime(track_duration_s))
    return track_duration_formatted

def track_feature_mode(track_audio_features):
    """
    Função de apoio para conversão de valores do `dict` contendo ``mode`` . ``0`` para ``Minor`` e ``1`` para ``Major``.

    :param track_audio_features: `dict` gerado por ``track`` contendo chave ``mode``.
    :type track_audio_features: `dict{int}`
    :return: Conversão de ``0`` para ``Minor`` e ``1`` para ``Major``.
    :rtype: `str`
    """
    #Como "mode" retorna 0 ou 1, equivalentes a "minor" e "major", podemos convertê-lo para uma string 
    mode = track_audio_features.get("mode")
    if mode == 0:
        mode = "Minor"
    elif mode == 1:
        mode =  "Major"
    else:
        mode = ""
        
    # A função retorna uma string com a exibição correta do modo da faixa
    return mode

def track_feature_key(track_audio_features):
    """
    Função de apoio para conversão de valores do `dict` contendo ``key`` seguindo a escala musical. ``0`` para ``C``, ``1`` para ``C♯/D♭``, assim em diante.

    :param track_audio_features: `dict` gerado por ``track`` contendo chave ``mode``.
    :type track_audio_features: `dict{int}`
    :return: Seguindo a escala musical, ``0`` para ``C``, ``1`` para ``C♯/D♭``, assim em diante.
    :rtype: `str`
    """
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
        key = ""
        
    # A função retorna uma string com a exibição correta do tom da faixa
    return key

def track_feature_timesig(track_audio_features):
    """
    Função de apoio para conversão de valores do `dict` contendo ``time_signature``. Os valores de ``time_signature`` contém números de 3 à 7, correspondendo aos tempos 3/4 a 7/4 respectivamente.

    :param track_audio_features: `dict` gerado por ``track`` contendo chave ``mode``.
    :type track_audio_features: `dict{int}`
    :return: Converte os valores de ``time_signature``, de 3 à 7, aos tempos 3/4 a 7/4 respectivamente.
    :rtype: `str`
    """
    #Como "timesig" retorna um número de 3 a 7, equivalentes a 3/4 até 7/4,
    timesig = track_audio_features.get("time_signature")
    timesig = f"{timesig}/4"
    
    # A função retorna uma string formatada com a exibição correta da divisão do tempo da faixa
    return timesig

# Função que coleta os dados de cada faixa de cada álbum
def artist_albums_track_data(sp, albums_data):
    """
    Pesquisa dentro da plataforma Spotify pelos dados de cada track em cada álbum e retorna uma lista de dicionários por track.

    :param sp: Objeto principal da API 
    :type sp: `<class 'spotipy.client.Spotify'>`
    :param albums_data: Lista de dicionários contendo dados dos álbuns
    :type albums_data: `list[dict]`
    :return: Lista de dicionários contendo dados de cada track
    :rtype: `list[dict]`
    """
    # Criação de lista para armazenamento  dos dados das faixas do artista de cada álbum
    tracks_data = list()    

    if type(albums_data) != list:
        raise Exception("albums_data aceita apenas listas")

    # Itera sobre cada álbum presente no albums_data (o próprio dict criado na função "artist_albums_data")
    for album in albums_data:
        print("\n", "Spotify ", "=-"*30, "\n", sep="")
        print("Analisando álbum:", album.get("name"))
        
        # Inicia um contador para armazenar e exibir o número de faixas processadas
        track_counter = 0
        
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
            except ConnectionError as error:
                print("Houve um problema de conexao")
                raise error
            except Exception as error:
                print("Houve um problema durante a execucao do projeto")
                raise error
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
                try:
                    track_audio_features = sp.audio_features(track_id)[0]
                except ConnectionError as error:
                    print("Houve um problema de conexao")
                    raise error
                except Exception as error:
                    print("Houve um problema durante a execucao do projeto")
                    raise error

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
                print(track_counter, "-", track_name)

                track_count_album +=1
            # Checa se ainda há mais álbuns a serem buscados    
            if tracks.get("next") == None:
                break
            i += 50

    # A função retorna uma lista de dicionários, onde cada elemento corresponde aos dados de uma faixa do artista
    return tracks_data

# Gera um dataframe a partir dos dados coletados, com a opção de salvar o dataframe num arquivo ".csv"
def generate_dataframe(artist_name, tracks_data, save_csv = False, save_to=""):
    """
    Função que gera um dataframe a partir dos dados das tracks no formato de listas de dicionários contendo os dados, caso ``save_csv = True``, um arquivo .csv será gerado em caminho pré-definido e informado por console. 

    :param artist_name: Nome do artista
    :type artist_name: `str`
    :param tracks_data: Lista de dicionários contendo dados das tracks
    :type tracks_data: `list[dict]`
    :param save_csv: Valor booleano que caso ``True``, irá gerar um arquivo .csv, padrão ``False``
    :type save_csv: ``bool``, opcional
    :param save_to: Path para o qual o arquivo criado será salvo
    :type save_to: `str`
    :return: Dataframe com os dados das tracks
    :rtype: `pandas.core.frame.DataFrame`
    """
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
        # Salva o dataframe num arquivo ".csv"
        tracks_dataframe.to_csv(save_to, sep=";", encoding="utf-8-sig", index=False)
        # Exibe uma mensagem de sucesso e exibe o local do arquivo gerado
        print("\nO arquivo 'spotify_data.csv' foi gerado e salvo em:\n", os.path.abspath(save_to), "\n", sep=";")

    # A função retorna o dataframe gerado a partir dos dados coletados
    return tracks_dataframe

# Função principal, que recolhe as credenciais e os parâmetros do usuário e executa todo o processo de obtenção de dados a partir da API do Spotify
def get_spotify_data(client_id, client_secret, artist_name, get_singles = False, duplicate = False, save_csv = False, save_to=""):
    """
    Função principal que irá ser utilizada pelo usuário diretamente, a qual irá coletar dados das músicas e álbuns de um determinado artista dentro da plataforma Spotify,

    :param client_id: Cadeia de caracteres alfa-numérica única para cada cliente gerada pela plataforma Spotify representando seu ID.
    :type client_id: `str`
    :param client_secret: Cadeia de caracteres alfa-numérica única para cada cliente gerada pela plataforma Spotify representando seu secret.
    :type client_secret: `str`
    :param artist: Artista escolhido 
    :type artist: `str`
    :param get_singles: Valor booleano opcional que caso seja ``True``, será pesquisado informações sobre álbuns single, padrão como ``False``.
    :type get_singles: `bool`, opcional
    :param duplicate: Valor booleano opcional que caso seja ``True``, não será desconsiderado duplicatas de álbuns, padrão como ``False``.
    :type duplicate: `bool`, opcional
    :param save_csv: Valor booleano que caso ``True``, irá gerar um arquivo .csv, padrão ``False``
    :type save_csv: ``bool``, opcional
    :param save_to: Path para o qual o arquivo criado será salvo
    :type save_to: `str`
    :return: Dataframe com os dados das tracks
    :rtype: `pandas.core.frame.DataFrame`
    """
    # Utiliza as credenciais do usuário para se autenticar e gerar o objeto principal da API do Spotify
    client_credentials_manager = autentication(client_id, client_secret)
    sp = spotify_object(client_credentials_manager)
    
    # Obtém os dados relacionados ao artista, aos seus álbuns e às suas músicas
    artist_name = get_artist_name(sp, artist_name)
    artist_id = get_artist_id(sp, artist_name)
    albums_data = artist_albums_data(sp, artist_id, get_singles, duplicate)
    tracks_data = artist_albums_track_data(sp, albums_data)
    
    # Organiza os dados coletados em um dataframe
    df = generate_dataframe(artist_name, tracks_data, save_csv, save_to)
    
    # A função retorna um dataframe com os dados coletados no Spotify sobre o artista escolhido
    return  df
