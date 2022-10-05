import os

import lyricsgenius
import pandas as pd

# Extrai os dados do artista através do seu nome
def get_artist_info(artist_name, genius):
    # Realiza uma busca pelo nome do artista
    artist = genius.search_artist(artist_name, max_songs=0, get_full_info=False)
    
    # Retorna o nome e o id do artista na plataforma Genius
    return artist.name, artist.id

# Extrai os dados dos álbums através do id do artista
def get_albums_info(artist_id, genius):
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
            # Extrai o nome, id e data de lançamento do álbum
            album_name = album.get("name")
            album_id = album.get("id")
            album_release_date = date_components_to_datetime(album.get("release_date_components"), album_name, "Álbum")
            
            # Armazena esses dados num dicionario
            album_dict = {"Album ID": album_id,
                          "Album Name": album_name,
                          "Release Date": album_release_date}
            
            # Adiciona o dicionário gerado à lista de álbuns
            albums_list.append(album_dict)
            
    # Retorna a lista de álbums gerada
    return albums_list

# Extrai as principais informações sobre uma faixa
def extract_track_info(track, genius):
    # Extrai o número da faixa
    track_number = track.get("number")
    
    # Acessa os metadados da faixa
    track_data = track.get("song")
    
    # Extrai o nome, id e data de lançamento da faixa
    track_name = track_data.get("title")
    track_id = track_data.get("id")
    track_release_date = date_components_to_datetime(track_data.get("release_date_components"), track_name, "Faixa")
    track_instrumental = is_instrumental(track_data.get("instrumental"))
    
    # Tenta obter a letra da música
    try:
        track_dict = genius.search_song(song_id=track_id, get_full_info=False)
        track_lyrics = track_dict.lyrics
        
    # Caso ocorra alguma exceção, consideraremos que nenhuma letra foi encontrada para a música
    except AttributeError:
        track_lyrics = ""
    
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)
        track_lyrics = ""
        
    # Retorna o número, nome, id, data de lançamento e a letra da faixa
    return track_number, track_name, track_id, track_release_date, track_instrumental, track_lyrics

# Extrai os dados de cada faixa através do id do álbum
def get_tracks_info(albums, genius):
    # Inicializa um contador de faixas processadas
    track_counter = 0
    
    # Inicializa uma lista para armazenar as faixas
    tracks = []
    
    # Itera sobre cada álbum
    for album in albums:
        # Acessa as informações de cada álbum
        album_id = album.get("Album ID")
        album_name = album.get("Album Name")
        album_release_date = album.get("Release Date")
        
        print("\n", "Genius ", "=-"*30, "\n", sep="")
        print("Analisando álbum:", album_name)
        
        # Coleta a lista de faixas de cada álbum a partir de seu id
        album_tracks = genius.album_tracks(album_id)
        
        # Itera sobre cada faixa do album
        for track in album_tracks.get("tracks"):
            
            # Extrai as seguintes informações dos dados da faixa
            track_number, track_name, track_id, track_release_date, track_instrumental, track_lyrics = extract_track_info(track, genius)
            
            # Tenta converter o track_number para inteiro
            try:
                track_number = int(track_number)
            # Caso ocorra algum erro (ex: track_number = None), considera que se trata da primeira faixa do álbum
            except:
                track_number = 1
                
            # Armazena os dados coletados num dicionário
            track_dict = {"Album Name": album_name,
                          "Release Date": album_release_date,
                           "Track Number": int(track_number),
                           "Track Name": track_name,
                           #"Track Release Date": track_release_date,
                           "Track Instrumental": track_instrumental,
                           "Track Lyrics": track_lyrics}
            
            # Adiciona o dicionário gerado à lista de faixas
            tracks.append(track_dict)
            
            # Incrementa e exibe o contador e o nome da faixa processada
            track_counter += 1
            print(track_counter, "-", track_name)
            
    # A função retorna uma lista de dicionários, onde cada dicionário contém os dados que descrevem cada faixa
    return tracks

# Gera um dataframe a partir dos dados coletados, com a opção de salvar o dataframe num arquivo ".csv"
def generate_dataframe(artist_name, tracks, save_csv = False):
    # Obtém o nome das colunas do dataframe a partir dos dados que cada faixa possui
    dataframe_columns = list(tracks[0].keys())

    # Inicializa uma lista para acumular os dados de cada faixa
    track_list = []
    
    # Itera sobre cada faixa, coletando seus dados e acumulando na lista criada
    for track in tracks:
        track_list.append(list(track.values()))
        
    # Gera um pandas DataFrame a partir dos dados coletados
    tracks_dataframe = pd.DataFrame(data=track_list, columns=dataframe_columns)
    
    # Caso o usuário deseje salvar o dataframe num arquivo ".csv"
    if save_csv:
        # Gera um caminho relativo, com o nome do artista
        csv_path = "genius_data.csv"
        
        # Salva o dataframe num arquivo ".csv"
        tracks_dataframe.to_csv(csv_path, sep=";", encoding="utf-8-sig", index=False)
        # Exibe uma mensagem de sucesso e exibe o local do arquivo gerado
        print("\nO arquivo 'genius_data.csv' foi gerado e salvo em:\n", os.path.abspath(csv_path), "\n", sep=";")

    # A função retorna o dataframe gerado
    return tracks_dataframe

# Gera um datetime a partir de seus componentes (ano, mês e dia)
def date_components_to_datetime(date_components, content_name, content_type):
    # Tenta converter os componentes da data de lançamento (dia, mês e ano) num único datetime
    try:
        datetime = lyricsgenius.utils.convert_to_datetime(date_components).date()
    
    # Caso ocorra algum erro durante a conversão ou a API não disponibilize a data de lançamento da faixa
    except Exception as e:
        datetime = None
        print(f"Ocorreu um erro inesperado durante a analise da data de lançamento de: {content_name} ({content_type}):\n{e}", sep="")
    
    # Retorna o datetime gerado a partir dos componentes (ano, mês e dia)
    return datetime

def is_instrumental(track_instrumental):
    if track_instrumental == True:
        track_instrumental_str = "Yes"
    else:
        track_instrumental_str = "No"
    return track_instrumental_str

# Utiliza a API do Genius e as funções acima para gerar um dataframe com as faixas e suas respectivas letras de um artista
def get_lyrics_of(artist_name, access_token="", save_csv = False):
    # Instancia o objeto principal da API do Genius
    genius_object = lyricsgenius.Genius(access_token, timeout=60, retries=10, 
                                  verbose=False, remove_section_headers=True)
    
    # Obtém o nome e o id do artista
    artist_name, artist_id = get_artist_info(artist_name, genius_object)
    
    # Obtém uma lista de álbuns, contendo seu nome e id do álbum
    albums = get_albums_info(artist_id, genius_object)
    
    # Obtém uma lista de faixas, contendo seu álbum, seu número, seu nome, sua data de lançamento e sua letra
    tracks = get_tracks_info(albums, genius_object)
    
    # Gera um dataframe contendo os dados coletados a partir da API da Genius
    tracks_dataframe = generate_dataframe(artist_name, tracks, save_csv)
    
    # Retorna um dataframe, contendo dados sobre o álbum, sobre a faixa, e sua letra
    return tracks_dataframe

