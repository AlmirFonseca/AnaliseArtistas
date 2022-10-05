from modules import spotify_artist_dataframe as sp
from modules import deezer_artist_dataframe as dz
from modules import genius_lyrics_dataframe as ge
from modules import merge_algorithm as ma

from modules import fix_lyricsgenius as fix

import os

# Define o nome do artista a ser analisado
artist_name = "Coldplay"

# Define as credenciais para o uso da API do Spotify
sp_client_id = "6a1edef9875b4c79a81e70db08f91c79"
sp_client_secret = "bd17a1c083284bd4882f1c0839a6df65"

# Define a credencial para o uso da API da Genius
ge_access_token = "u2SqMOrCtzWwY9xGxI6PiLn5aVqnhzWMiaMWB2BmrfuvJQL-Z_nQ4pv8gJej4isU"

def generate_dataframe_of(artist_name, sp_client_id, sp_client_secret, ge_access_token="", save_csv=True, filter_terms="", append_genre=True, append_lyrics=True):

    # SPOTIFY ##############################################################################
    
    # Obtém um dataframe com os dados do artista, seus álbums e suas músicas no Spotify
    df_spotify = sp.get_spotify_data(sp_client_id, sp_client_secret, artist_name, get_singles=True, duplicate=False, save_csv=True)
    
    # Filtra os álbuns através da busca por termos específicos em seus títulos
    df_spotify = ma.filter_dataframe(df_spotify, "Album Name", filter_terms)
    
    # Normaliza os nomes dos álbuns a fim de permitir uma assimilação direta
    df_spotify["Normalized Album Name"] = ma.normalize_content(df_spotify["Album Name"])
    # Caso não sobre nenhum caractere válido no nome do álbum após a normalização, esse álbum é descartado
    df_spotify.dropna(subset=["Normalized Album Name"], inplace=True)
    
    if save_csv:
        # Salva o dataframe já filtrado num arquivo .csv
        df_spotify.to_csv("spotify_data_filtered.csv", encoding="utf-8-sig", sep=";", index=False)
    
    # Caso o usuário deseje adicionar dados dos gêneros dos álbuns, será realizada uma coleta dos dados na plataforma Deezer
    if append_genre:
    
        # DEEZER ##############################################################################
        
        # Obtém um dataframe com os dados do artista, seus álbums e suas músicas na Deezer
        df_deezer = dz.discography(artist_name, save_csv=True)
        
        # Filtra os álbuns através da busca por termos específicos em seus títulos
        df_deezer = ma.filter_dataframe(df_deezer, "Album Name", filter_terms)
        
        # Normaliza os nomes dos álbuns a fim de permitir uma assimilação direta
        df_deezer["Normalized Album Name"] = ma.normalize_content(df_deezer["Album Name"])
        # Caso não sobre nenhum caractere válido no nome do álbum após a normalização, esse álbum é descartado
        df_deezer.dropna(subset=["Normalized Album Name"], inplace=True)
        
        # Caso o usuário opte por salvar os dataframes em arquivos ".csv"
        if save_csv:
            # Salva o dataframe já filtrado num arquivo .csv
            df_deezer.to_csv("deezer_data_filtered.csv", encoding="utf-8-sig", sep=";", index=False)
            
        # Adiciona os dados de gênero ao dataframe do spotify
        df_spotify = ma.append_genre(df_spotify, df_deezer)
    
    # Caso o usuário deseje adicionar dados das letras das músicas, será realizada uma coleta dos dados na plataforma Genius
    if append_lyrics:
    
        # GENIUS ##############################################################################
    
        # Obtém um dataframe com os dados do artista, seus álbums e suas músicas e suas letras na Genius
        df_genius = ge.get_lyrics_of(artist_name, ge_access_token, save_csv=True)
        
        # Filtra os álbuns através da busca por termos específicos em seus títulos
        df_genius = ma.filter_dataframe(df_genius, "Album Name", filter_terms)
        
        # Normaliza os nomes dos álbuns a fim de permitir uma assimilação direta
        df_genius["Normalized Album Name"] = ma.normalize_content(df_genius["Album Name"])
        # Caso não sobre nenhum caractere válido no nome do álbum após a normalização, esse álbum é descartado
        df_genius.dropna(subset=["Normalized Album Name"], inplace=True)
        
        # Caso o usuário opte por salvar os dataframes em arquivos ".csv"
        if save_csv:
            # Salva o dataframe já filtrado num arquivo .csv
            df_genius.to_csv("genius_data_filtered.csv", encoding="utf-8-sig", sep=";", index=False)
            
        df_spotify = ma.append_lyrics_and_instrumental(df_spotify, df_genius)
        
    # Caso o usuário opte por salvar os dataframes em arquivos ".csv"
    if save_csv:
        # Gera um caminho relativo, com o nome do artista
        csv_path = "artist_data.csv"
        
        # Salva o dataframe num arquivo ".csv"
        df_spotify.to_csv(csv_path, sep=";", encoding="utf-8-sig", index=False)
        # Exibe uma mensagem de sucesso e exibe o local do arquivo gerado
        print("\nO arquivo 'artist_data.csv' foi gerado e salvo em:\n", os.path.abspath(csv_path), "\n", sep=";")
    
    return df_spotify

coldplay_data = generate_dataframe_of(artist_name, sp_client_id, sp_client_secret, ge_access_token, filter_terms="live, remix")

    










