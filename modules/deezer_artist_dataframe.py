# Importa as bibliotecas necess√°rias 
import os
import deezer
import pandas as pd
import time

# Recebe o nome de um artista ou banda e retorna seus dados extra√≠dos da plataforma Deezer
def artist_info(searched_artist):
    client = deezer.Client() #Sincroniza com a plataforma 
    artist = client.search_artists(searched_artist)[0] #Retorna o primeiro resultado para o artista pesquisado
    artist_name = artist.name
    artist_nb_album = artist.nb_album
    artist_nb_fans = artist.nb_fan
    artist_albums = artist.get_albums()
    return artist_name, artist_nb_album, artist_nb_fans, artist_albums

# Recebe um √°lbum e retorna os seus g√™neros em formato de string
def genres(album): 
    album_genres_list = []
    album_genres = album.genres
    for genre in album_genres:
        album_genres_list.append(genre.name) #Adiciona em uma lista os nomes dos g√™neros
    album_genres_str = "/".join(album_genres_list) #Transforma a lista em uma string
    return album_genres_str
    
# Recebe um √°lbum e retorna seus dados extra√≠dos da plataforma Deezer
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
    
# Recebe uma faixa e retorna a string "Yes" se ela for expl√≠cita e "No" se n√£o for
def is_explicit(track):
    track_explicit_lyrics=track.explicit_lyrics
    if track_explicit_lyrics == True:
        track_explicit_lyrics_str = "Yes"
    else:
        track_explicit_lyrics_str = "No"
    return track_explicit_lyrics_str

# Recebe uma faixa e retorna os dados de cada uma extra√≠dos da plataforma Deezer
def track_info(track):
    track_title = track.title
    track_duration = time.strftime("%M:%S", time.gmtime(track.duration))
    track_position = track.track_position
    track_disk_number = track.disk_number
    track_explicit_lyrics = is_explicit(track) #Utiliza a fun√ß√£o de apoio is_explicit
    track_gain = track.gain
    track_contributors = contribuitors(track) #Utiliza a fun√ß√£o de apoio contribuitors
    return track_title, track_duration, track_position, track_disk_number, track_explicit_lyrics, track_gain, track_contributors

# Gera um dataframe a partir dos dados coletados, com a opÁ„o de salvar o dataframe num arquivo ".csv"
def generate_dataframe(artist_name, tracks_data, save_csv = False, save_to=""):    
    # ObtÈm o nome das colunas do dataframe a partir dos dados que cada faixa possui
    dataframe_columns = list(tracks_data[0].keys())

    # Inicializa uma lista para acumular os dados de cada faixa
    track_list = []
    
    # Itera sobre cada faixa, coletando seus dados e acumulando na lista criada
    for track in tracks_data:
        track_list.append(list(track.values()))
        
    # Gera um pandas DataFrame a partir dos dados coletados
    tracks_dataframe = pd.DataFrame(data=track_list, columns=dataframe_columns)
    
    # Caso o usu·rio deseje salvar o dataframe num arquivo ".csv"
    if save_csv:
        # Salva o dataframe num arquivo ".csv"
        tracks_dataframe.to_csv(save_to, sep=";", encoding="utf-8-sig", index=False)
        # Exibe uma mensagem de sucesso e exibe o local do arquivo gerado
        print("\nO arquivo 'deezer_data.csv' foi gerado e salvo em:\n", os.path.abspath(save_to), "\n", sep=";")

    # A funÁ„o retorna o dataframe gerado a partir dos dados coletados
    return tracks_dataframe

#Utiliza as outras fun√ß√µes para criar um dataframe com informa√ß√µes da discografia do artista
def discography(artist, save_csv=False, save_to="", duplicate=False):
    try:
        song_data = list()
        # albums = artist_info(artist)[3]# Busca os √°lbuns do artista
        artist_name, artist_nb_album, artist_nb_fans, artist_albums = artist_info(artist) # Busca os √°lbuns do artista
        
        # CriaÁ„o de dicion·rio para armazenamento  dos dados dos ·lbuns do artista
        albums_data = {}
        
        for album in artist_albums:
            # Recolhe os principais dados de cada ·lbum
            album_title, album_genres, album_nb_tracks, album_fans, album_release_date, album_tracks = album_info(album) #Busca a informa√ß√£o de cada album
            
            # Armazena os dados num dicion·rio
            album_dict = { 
                        "name" : album_title,
                        "genres": album_genres,
                        "release_date" : album_release_date,
                        "num_tracks" : album_nb_tracks,
                        "fans": album_fans,
                        "tracks": album_tracks}
            
            if not duplicate:
                # Verifica a existÍncia de nome de ·lbum no dict gerado atÈ o momento
                if album_title in albums_data.keys():
                    # Caso exista, È acessado o nome do dicion·rio j· existente (old) e o novo, e a quantidade
                    # de tracks
                    num_tracks_album_old = albums_data.get(album_title).get("num_tracks")
                    num_tracks_album_new = album_nb_tracks
                    #Caso a quantidade de tracks do novo seja maior que o antigo È sobreescrito pelo novo
                    if num_tracks_album_new > num_tracks_album_old:
                        albums_data[album_title] = album_dict
                    else:
                    #Caso n„o seja, È ignorado e descartado
                        pass
                else:
                    #Caso n„o exista, È adicionado ao dicion·rio
                    albums_data[album_title] = album_dict
            else:
                # Acumula os dicion·rios no dicion·rio criado
                albums_data[album_title] = album_dict
            
        # Gera uma lista de dicion·rios, onde cada elemento armazena os dados de um ·lbum
        albums_data = list(albums_data.values())
        
        # Itera sobre os dicionarios da lista gerada
        for album in albums_data:
            
            # Extrai informaÁıes b·sicas de cada ·lbum
            album_title = album.get("name")
            album_genres = album.get("genres")
            album_release_date = album.get("release_date")
            
            # Extrai o dicion·rio de dados sobre as faixas
            album_tracks = album.get("tracks")
            
            print("\n", "Deezer ", "=-"*30, "\n", sep="")
            print("Analisando album:", album_title)
            
            # Inicia um contador de faixas processadas
            track_counter = 0
            
            # Busca as faixas em um √°lbum
            for track in album_tracks:
                track_title, track_duration, track_position, track_disk_number, track_explicit_lyrics, track_gain, track_contributors = track_info(track) #Busca a informa√ß√£o de cada faixa
                
                # Incrementa o contador de faixas e imprime um log de progresso
                track_counter += 1
                print(track_counter, "-", track_title)
                
                # Caso haja discos com mais de um CD, utiliza o contador de faixas para determinar o n˙mero das faixas
                if track_disk_number > 1:
                    track_position = track_counter
                    
                # Gera um dicion·rio para cada faixa, organizando os dados coletados
                track_dict = {"Album Name": album_title,
                              "Genre": album_genres,
                              "Release Date": album_release_date,
                              "Track Number": track_position,
                              "Track Name": track_title,
                              "Artist Names": track_contributors,
                              "Duration": track_duration,
                              "Explicit": track_explicit_lyrics,
                              "Gain": track_gain}
                
                # O dicion·rio de cada faixa È concatenado ‡ lista de dicion·rios
                song_data.append(track_dict)
                
    except TypeError as te: #Avisa ao usu√°rio caso a fun√ß√£o n√£o receba uma string
        print("Essa fun√ß√£o deve receber uma string;",te)
    except IndexError as ie: #Avisa ao usu√°rio caso o artista procurado n√£o seja encontrado
        print("Artista n√£o encontrado;",ie)
    else: 
        # Caso n„o haja nenhum erro na aquisiÁ„o dos dados, È gerado um dataframe a partir dos dados coletados
        df_discografia = generate_dataframe(artist_name, song_data, save_csv, save_to=save_to)
        
        # A funÁ„o retorna um dataframe com todos os dados do artista coletados a partir da plataforma Deezer
        return df_discografia