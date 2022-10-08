# Importa as bibliotecas necessÃ¡rias 
import os
import deezer
import pandas as pd
import time

# Recebe o nome de um artista ou banda e retorna seus dados extraidos da plataforma Deezer
def artist_info(searched_artist):
    """
    Extrai dados da plataforma Deezer sobre determinado artista

    :param searched_artist: Artista sobre o qual serão extraídos os dados da plataforma Deezer
    :type searched_artist: `str`
    :return: Tupla contendo nome oficial na plataforma, número de álbuns, número de fãs e álbuns do artista
    :rtype: `tuple(str, int, int, <class 'deezer.pagination.PaginatedList'>)`
    """
    client = deezer.Client() #Sincroniza com a plataforma 
    artist = client.search_artists(searched_artist)[0] #Retorna o primeiro resultado para o artista pesquisado
    artist_name = artist.name
    artist_nb_album = artist.nb_album
    artist_nb_fans = artist.nb_fan
    artist_albums = artist.get_albums()
    return artist_name, artist_nb_album, artist_nb_fans, artist_albums

# Recebe um Ã¡lbum e retorna os seus gÃªneros em formato de string
def genres(album):
    """
    Pesquisa pelo genêro musical de um álbum dentro da plataforma Deezer

    :param album: Nome do álbum a ser pesquisado o genêro musical 
    :type album: `str`
    :return: Genêro musical do álbum 
    :rtype: `str`
    """
    album_genres_list = []
    album_genres = album.genres
    for genre in album_genres:
        album_genres_list.append(genre.name) #Adiciona em uma lista os nomes dos gÃªneros
    album_genres_str = "/".join(album_genres_list) #Transforma a lista em uma string
    return album_genres_str
    
# Recebe um Ã¡lbum e retorna seus dados extraÃ­dos da plataforma Deezer
def album_info(album):
    """
    Coleta dados sobre as informações de um determinado álbum

    :param album: Nome do álbum a ser coletado as informações
    :type album: `str`
    :return: Tupla com título, gêneros, número de tracks, número de fãs, data de lançamento e nome de todas as faixas em uma lista
    :rtype: `tuple(str, str, int, int, str, list[str])`
    """
    album_title = album.title
    album_genres = genres(album)
    album_nb_tracks = album.nb_tracks
    album_fans = album.fans
    album_release_date = album.release_date.strftime("%d/%m/%Y")
    album_tracks = album.tracks
    return album_title, album_genres, album_nb_tracks, album_fans, album_release_date, album_tracks
    
    
# Recebe uma faixa e retorna os seus contribuintes em formato de string
def contribuitors(track):
    """
    Pesquisa pelos contribuidores e autores de uma determina faixa

    :param track: Nome da faixa a ser pesquisada os contribuidores e autores
    :type track: `str`
    :return: Contribuidores e autores da faixa
    :rtype: `str`
    """
    track_contributors = track.contributors 
    track_contributors_list = []
    for contributor in track_contributors:
        track_contributors_list.append(contributor.name) #Adiciona em uma lista os nomes dos contribuintes
        track_contributors_str = "/".join(track_contributors_list)#Transforma a lista em uma string
    return track_contributors_str
    
# Recebe uma faixa e retorna a string "Yes" se ela for explÃ­cita e "No" se nÃ£o for
def is_explicit(track):
    """
    Pesquisa se uma determinada faixa tem conteúdo explícito 

    :param track: Nome da faixa a ser pesquisada se possui conteúdo explícito
    :type track: `str`
    :return: Situação da faixa em relação a presença de conteúdo explícito
    :rtype: `str`
    """
    track_explicit_lyrics=track.explicit_lyrics
    if track_explicit_lyrics == True:
        track_explicit_lyrics_str = "Yes"
    else:
        track_explicit_lyrics_str = "No"
    return track_explicit_lyrics_str

# Recebe uma faixa e retorna os dados de cada uma extraÃ­dos da plataforma Deezer
def track_info(track):
    """
    Função que coleta informações de uma determinada faixa

    :param track: Faixa a ser coletada informações
    :type track: `str`
    :return: Tupla contendo título, duração, posição, número de disco, se há conteúdo explícito, ganho e contribuidores.
    :rtype: tuple(str, str, int, int, str, int, str)
    """
    track_title = track.title
    track_duration = time.strftime("%M:%S", time.gmtime(track.duration))
    track_position = track.track_position
    track_disk_number = track.disk_number
    track_explicit_lyrics = is_explicit(track) #Utiliza a funÃ§Ã£o de apoio is_explicit
    track_gain = track.gain
    track_contributors = contribuitors(track) #Utiliza a funÃ§Ã£o de apoio contribuitors
    return track_title, track_duration, track_position, track_disk_number, track_explicit_lyrics, track_gain, track_contributors

# Gera um dataframe a partir dos dados coletados, com a opção de salvar o dataframe num arquivo ".csv"
def generate_dataframe(artist_name, tracks_data, save_csv = False, save_to=""):
    """
    Gera um dataframe a partir dos dados das tracks coletados pelas outras funções do módulo

    :param artist_name: Nome do artista 
    :type artist_name: `str`
    :param tracks_data: Lista de dicionários contendo dados das faixas
    :type tracks_data: `list[dict]`
    :param save_csv: Valor booleano para criação de um arquivo csv, padrão como False
    :type save_csv: `bool`, opcional
    :param save_to: Path para o qual o arquivo criado será salvo
    :type save_to: `str`
    :return: Dataframe contendo informações sobre as tracks de um artista na plataforma deezer
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
        print("\nO arquivo 'deezer_data.csv' foi gerado e salvo em:\n", os.path.abspath(save_to), "\n", sep=";")

    # A função retorna o dataframe gerado a partir dos dados coletados
    return tracks_dataframe

#Utiliza as outras funÃ§Ãµes para criar um dataframe com informaÃ§Ãµes da discografia do artista
def discography(artist, save_csv=False, save_to="", duplicate=False):
    """
    Função principal a ser utilizada que coleta dados da discografia de um determinado artista e retorna um dataframe contendo informações dos álbuns 
    e faixas, como também, pode salvar um arquivo .csv de preferência do usuário.

    :param artist: Artista a ser pesquisado e coletado os dados de sua discografia
    :type artist: `str`
    :param save_csv: Valor booleano para criação de um arquivo csv, padrão como False
    :type save_csv: `bool`, opcional
    :param save_to: Path para o qual o arquivo criado será salvo
    :type save_to: `str`
    :return: Dataframe contendo informações sobre discografia do artista
    :rtype: `pandas.core.frame.DataFrame`
    """
    try:
        song_data = list()
        # albums = artist_info(artist)[3]# Busca os Ã¡lbuns do artista
        artist_name, artist_nb_album, artist_nb_fans, artist_albums = artist_info(artist) # Busca os Ã¡lbuns do artista
        
        # Criação de dicionário para armazenamento  dos dados dos álbuns do artista
        albums_data = {}
        
        for album in artist_albums:
            # Recolhe os principais dados de cada álbum
            album_title, album_genres, album_nb_tracks, album_fans, album_release_date, album_tracks = album_info(album) #Busca a informaÃ§Ã£o de cada album
            
            # Armazena os dados num dicionário
            album_dict = { 
                        "name" : album_title,
                        "genres": album_genres,
                        "release_date" : album_release_date,
                        "num_tracks" : album_nb_tracks,
                        "fans": album_fans,
                        "tracks": album_tracks}
            
            if not duplicate:
                # Verifica a existência de nome de álbum no dict gerado até o momento
                if album_title in albums_data.keys():
                    # Caso exista, é acessado o nome do dicionário já existente (old) e o novo, e a quantidade
                    # de tracks
                    num_tracks_album_old = albums_data.get(album_title).get("num_tracks")
                    num_tracks_album_new = album_nb_tracks
                    #Caso a quantidade de tracks do novo seja maior que o antigo é sobreescrito pelo novo
                    if num_tracks_album_new > num_tracks_album_old:
                        albums_data[album_title] = album_dict
                    else:
                    #Caso não seja, é ignorado e descartado
                        pass
                else:
                    #Caso não exista, é adicionado ao dicionário
                    albums_data[album_title] = album_dict
            else:
                # Acumula os dicionários no dicionário criado
                albums_data[album_title] = album_dict
            
        # Gera uma lista de dicionários, onde cada elemento armazena os dados de um álbum
        albums_data = list(albums_data.values())
        
        # Itera sobre os dicionarios da lista gerada
        for album in albums_data:
            
            # Extrai informações básicas de cada álbum
            album_title = album.get("name")
            album_genres = album.get("genres")
            album_release_date = album.get("release_date")
            
            # Extrai o dicionário de dados sobre as faixas
            album_tracks = album.get("tracks")
            
            print("\n", "Deezer ", "=-"*30, "\n", sep="")
            print("Analisando album:", album_title)
            
            # Inicia um contador de faixas processadas
            track_counter = 0
            
            # Busca as faixas em um Ã¡lbum
            for track in album_tracks:
                track_title, track_duration, track_position, track_disk_number, track_explicit_lyrics, track_gain, track_contributors = track_info(track) #Busca a informaÃ§Ã£o de cada faixa
                
                # Incrementa o contador de faixas e imprime um log de progresso
                track_counter += 1
                print(track_counter, "-", track_title)
                
                # Caso haja discos com mais de um CD, utiliza o contador de faixas para determinar o número das faixas
                if track_disk_number > 1:
                    track_position = track_counter
                    
                # Gera um dicionário para cada faixa, organizando os dados coletados
                track_dict = {"Album Name": album_title,
                              "Genre": album_genres,
                              "Release Date": album_release_date,
                              "Track Number": track_position,
                              "Track Name": track_title,
                              "Artist Names": track_contributors,
                              "Duration": track_duration,
                              "Explicit": track_explicit_lyrics,
                              "Gain": track_gain}
                
                # O dicionário de cada faixa é concatenado à lista de dicionários
                song_data.append(track_dict)
                
    except TypeError as te: #Avisa ao usuÃ¡rio caso a funÃ§Ã£o nÃ£o receba uma string
        print("Essa funÃ§Ã£o deve receber uma string;",te)
    except IndexError as ie: #Avisa ao usuÃ¡rio caso o artista procurado nÃ£o seja encontrado
        print("Artista nÃ£o encontrado;",ie)
    else: 
        # Caso não haja nenhum erro na aquisição dos dados, é gerado um dataframe a partir dos dados coletados
        df_discografia = generate_dataframe(artist_name, song_data, save_csv, save_to=save_to)
        
        # A função retorna um dataframe com todos os dados do artista coletados a partir da plataforma Deezer
        return df_discografia
