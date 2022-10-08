# Artist Dataframe Generator
''' Módulo de criação de dataframe final
    -------------------------------------

Esse módulo contém funções responsáveis por gerar um dataframe a partir dos dados das 
plataformas Spotify, Deezer e LyricsGenius, já que há informações exclusivas em cada plataforma, foi necessário
juntar os resultados e formar um dataframe geral.

'''

import os
import sys

import re

sys.path.insert(0, 'modules')

import deezer_artist_dataframe as dz
import genius_lyrics_dataframe as ge
import merge_algorithm as ma
import spotify_artist_dataframe as sp

# Cria as pastas aonde os arquivos gerados serão salvos
def prepare_results_folder(artist_name):
    """
    Cria pastas aonde os arquivos gerados durante a execução das funções serão salvos

    :param artist_name: Nome do artista
    :type artist_name: `str`
    :return: Função retorna caminhos absolutos das pastas criadas em uma tupla
    :rtype: `tuple(str, str, str, str)`
    """
    # Obtém o caminho para a pasta raiz do projeto
    root_path = os.path.abspath(os.getcwd())
    
    # Obtém o caminho para a pasta de resultados
    results_path = os.path.join(root_path, "results")
    # Caso a pasta de resultados não exista, ela é criada
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    
    # Trata o nome do artista para que seja gerado um caminho valido a partir do nome do artista
    artist_name = re.sub("[^A-Za-z0-9 ]+", "", artist_name)
    artist_name = artist_name.upper()
    
    # Cria uma pasta, com o nome do artista, aonde serão salvos todos os arquivos
    artist_results_folder = os.path.join(results_path, artist_name)
    if not os.path.exists(artist_results_folder):
        os.mkdir(artist_results_folder)
        
    # Cria pastas secundárias aonde serão armazenados os arquivos secundários/temporários do projeto, uma para cada plataforma
    spotify_results_folder = os.path.join(artist_results_folder, "spotify")
    if not os.path.exists(spotify_results_folder):
        os.mkdir(spotify_results_folder)
        
    deezer_results_folder = os.path.join(artist_results_folder, "deezer")
    if not os.path.exists(deezer_results_folder):
        os.mkdir(deezer_results_folder)
        
    genius_results_folder = os.path.join(artist_results_folder, "genius")
    if not os.path.exists(genius_results_folder):
        os.mkdir(genius_results_folder)
    
    # A função retorna os caminhos absolutos das pastas criadas
    return artist_results_folder, spotify_results_folder, deezer_results_folder, genius_results_folder

# Obtém e filtra um dataframe com os dados do artista, seus álbums e suas músicas no Spotify
def get_spotify_data(artist_name, sp_client_id, sp_client_secret, filter_terms="", save_csv=True, save_to=""):
    """
    Cria um dataframe com os dados do artista, álbuns e músicas dentro da plataforma Spotify, 
    além de filtrá-lo e salvar em um arquivo .csv se for da preferência do usuário

    :param artist_name: Nome do artista
    :type artist_name: `str`
    :param sp_client_id: Id de cliente na API da plataforma Spotify
    :type sp_client_id: `str`
    :param sp_client_secret: Secret de cliente na API da plataforma Spotify 
    :type sp_client_secret: `str`
    :param filter_terms: Termos específicos a serem utilizados como filtro nos títulos dos álbuns, padrão como ``""``
    :type filter_terms: `str`, opcional
    :param save_csv: Valor booleano para criação de um arquivo csv, padrão como False
    :type save_csv: `bool`, opcional
    :param save_to: Path para o qual o arquivo criado será salvo
    :type save_to: `str`
    :return: Dataframe com os dados do artista, álbuns e músicas dentro da plataforma Spotify
    :rtype: `pandas.core.frame.DataFrame`
    """
    # Prepara o caminho dos arquivos a serem gerados
    sp_data_path = os.path.join(save_to, "spotify_data.csv")
    sp_data_filtered_path = os.path.join(save_to, "spotify_data_filtered.csv")
    
    # Obtém um dataframe com os dados do artista, seus álbums e suas músicas no Spotify
    df_spotify = sp.get_spotify_data(sp_client_id, sp_client_secret, artist_name, get_singles=True, duplicate=False, save_csv=True, save_to=sp_data_path)
    
    # Filtra os álbuns através da busca por termos específicos em seus títulos
    df_spotify = ma.filter_dataframe(df_spotify, "Album Name", filter_terms)
    
    # Normaliza os nomes dos álbuns a fim de permitir uma assimilação direta
    df_spotify["Normalized Album Name"] = ma.normalize_content(df_spotify["Album Name"])
    # Caso não sobre nenhum caractere válido no nome do álbum após a normalização, esse álbum é descartado
    df_spotify.dropna(subset=["Normalized Album Name"], inplace=True)
    
    if save_csv:
        # Salva o dataframe já filtrado num arquivo .csv
        df_spotify.to_csv(sp_data_filtered_path, encoding="utf-8-sig", sep=";", index=False)
        
    # A função retorna o dataframe dos dados coletados sobre o artista a partir da plataforma Spotify
    return df_spotify
    
# Obtém e filtra um dataframe com os dados do artista, seus álbums e suas músicas na Deezer
def get_deezer_data(artist_name, filter_terms, save_csv=True, save_to=""):
    """
    Cria um dataframe com os dados do artista, álbuns e músicas dentro da plataforma Deezer, 
    além de filtrá-lo e salvar em um arquivo .csv se for da preferência do usuário

    :param artist_name: Nome do artista
    :type artist_name: `str`
    :param filter_terms: Termos específicos a serem utilizados como filtro nos títulos dos álbuns, padrão como ``""``
    :type filter_terms: `str`, opcional
    :param save_csv: Valor booleano para criação de um arquivo csv, padrão como False
    :type save_csv: `bool`, opcional
    :param save_to: Path para o qual o arquivo criado será salvo
    :type save_to: `str`
    :return: Dataframe com os dados do artista, álbuns e músicas dentro da plataforma Deezer
    :rtype: `pandas.core.frame.DataFrame`
    """
    # Prepara o caminho dos arquivos a serem gerados
    dz_data_path = os.path.join(save_to, "deezer_data.csv")
    dz_data_filtered_path = os.path.join(save_to, "deezer_data_filtered.csv")
    
    # Obtém um dataframe com os dados do artista, seus álbums e suas músicas na Deezer
    df_deezer = dz.discography(artist_name, save_csv=True, save_to=dz_data_path)
    
    # Filtra os álbuns através da busca por termos específicos em seus títulos
    df_deezer = ma.filter_dataframe(df_deezer, "Album Name", filter_terms)
    
    # Normaliza os nomes dos álbuns a fim de permitir uma assimilação direta
    df_deezer["Normalized Album Name"] = ma.normalize_content(df_deezer["Album Name"])
    # Caso não sobre nenhum caractere válido no nome do álbum após a normalização, esse álbum é descartado
    df_deezer.dropna(subset=["Normalized Album Name"], inplace=True)
    
    # Caso o usuário opte por salvar os dataframes em arquivos ".csv"
    if save_csv:
        # Salva o dataframe já filtrado num arquivo .csv
        df_deezer.to_csv(dz_data_filtered_path, encoding="utf-8-sig", sep=";", index=False)
      
    # A função retorna o dataframe dos dados coletados sobre o artista a partir da plataforma Deezer
    return df_deezer

# Obtém e filtra um dataframe com os dados do artista, seus álbums e suas músicas na Genius
def get_genius_data(artist_name, ge_access_token, filter_terms, save_csv=True, save_to=""):
    """
    Cria um dataframe com os dados do artista, álbuns, músicas e letras dentro da plataforma LyricsGenius, 
    além de filtrá-lo e salvar em um arquivo .csv se for da preferência do usuário

    :param artist_name: Nome do artista
    :type artist_name: `str`
    :param ge_access_token: Token de acesso da plataforma LyricsGenius
    :type ge_access_token: `str`
    :param filter_terms: Termos específicos a serem utilizados como filtro nos títulos dos álbuns, padrão como ``""``
    :type filter_terms: `str`, opcional
    :param save_csv: Valor booleano para criação de um arquivo csv, padrão como False
    :type save_csv: `bool`, opcional
    :param save_to: Path para o qual o arquivo criado será salvo
    :type save_to: `str`
    :return: Dataframe com os dados do artista, álbuns, músicas e letras dentro da plataforma LyricsGenius
    :rtype: `pandas.core.frame.DataFrame`
    """
    # Prepara o caminho dos arquivos a serem gerados
    ge_data_path = os.path.join(save_to, "genius_data.csv")
    ge_data_filtered_path = os.path.join(save_to, "genius_data_filtered.csv")
    
    # Obtém um dataframe com os dados do artista, seus álbums e suas músicas e suas letras na Genius
    df_genius = ge.get_lyrics_of(artist_name, ge_access_token, save_csv=True, save_to=ge_data_path)
    
    # Filtra os álbuns através da busca por termos específicos em seus títulos
    df_genius = ma.filter_dataframe(df_genius, "Album Name", filter_terms)
    
    # Normaliza os nomes dos álbuns a fim de permitir uma assimilação direta
    df_genius["Normalized Album Name"] = ma.normalize_content(df_genius["Album Name"])
    # Caso não sobre nenhum caractere válido no nome do álbum após a normalização, esse álbum é descartado
    df_genius.dropna(subset=["Normalized Album Name"], inplace=True)
    
    # Caso o usuário opte por salvar os dataframes em arquivos ".csv"
    if save_csv:
        # Salva o dataframe já filtrado num arquivo .csv
        df_genius.to_csv(ge_data_filtered_path, encoding="utf-8-sig", sep=";", index=False)
    
    # A função retorna o dataframe dos dados coletados sobre o artista a partir da plataforma Genius
    return df_genius

def generate_dataframe_of(artist_name, sp_client_id, sp_client_secret, ge_access_token="", save_csv=True, filter_terms="", append_genre=True, append_lyrics=True):
    """
    A função que gera Dataframe a partir dos dados coletados do Spotify, 
    com as adições que o usuário escolher (gênero a partir da plataforma Deezer, instrumental e letras a partir da plataforma LyricsGenius)

    :param artist_name: Nome do artista
    :type artist_name: `str`
    :param sp_client_id: Id de cliente na API da plataforma Spotify
    :type sp_client_id: `str`
    :param sp_client_secret: Secret de cliente na API da plataforma Spotify 
    :type sp_client_secret: `str`
    :param ge_access_token: Token de acesso da plataforma LyricsGenius
    :type ge_access_token: `str`
    :param save_csv: Valor booleano para criação de um arquivo csv, padrão como False
    :type save_csv: `bool`, opcional
    :param filter_terms: Termos específicos a serem utilizados como filtro nos títulos dos álbuns, padrão como ``""``
    :type filter_terms: `str`, opcional
    :param append_genre: Valor booleano para caso o usuário deseje adicionar dados dos gêneros dos álbuns, padrão para True
    :type append_genre: `bool`, opcional
    :param append_lyrics: Valor booleano para caso o usuário deseje adicionar dados das letras dos álbuns, padrão para True
    :type append_lyrics: `bool`, opcional
    :return: Dataframe com os dados do artista, álbuns, músicas dentro da plataforma Spotify, além da adição dos dados das plataformas Deezer e LyricsGenius
    :rtype: `pandas.core.frame.DataFrame`
    """
    # Caso o usuário opte por salvar os dataframes em arquivos ".csv"
    if save_csv:
        results_folder, spotify_results_folder, deezer_results_folder, genius_results_folder = prepare_results_folder(artist_name)
    
    # Obtém um dataframe filtrado com os dados do artista, seus álbums e suas músicas na Deezer
    df_spotify = get_spotify_data(artist_name, sp_client_id, sp_client_secret, filter_terms, save_csv, save_to=spotify_results_folder)
    
    # Caso o usuário deseje adicionar dados dos gêneros dos álbuns, será realizada uma coleta dos dados na plataforma Spotify
    if append_genre:
        # Obtém e filtra um dataframe filtrado os dados do artista, seus álbums e suas músicas na Deezer
        df_deezer = get_deezer_data(artist_name, filter_terms, save_csv, save_to=deezer_results_folder)
        
        # Adiciona os dados de gênero ao dataframe do spotify
        df_spotify = ma.append_genre(df_spotify, df_deezer)
    
    # Caso o usuário deseje adicionar dados das letras das músicas, será realizada uma coleta dos dados na plataforma Genius
    if append_lyrics:
        # Obtém e filtra um dataframe filtrado os dados do artista, seus álbums e suas músicas na Genius
        df_genius = get_genius_data(artist_name, ge_access_token, filter_terms, save_csv, save_to=genius_results_folder)
        
        # Adiciona os dados de instrumentalidade e as letras das faixas ao dataframe do spotify 
        df_spotify = ma.append_lyrics_and_instrumental(df_spotify, df_genius)
        
    # Deleta colunas que armazenam dados temporários, úteis apenas para funções internas do módulo
    df_spotify.drop(["Album ID", "Normalized Album Name"], axis=1, inplace=True)
        
    # Caso o usuário opte por salvar os dataframes em arquivos ".csv"
    if save_csv:
        # Gera um caminho para salvar o arquivo com o resultado do processamento das músicas do artista
        csv_path = os.path.join(results_folder, "artist_data.csv")
        
        # Salva o dataframe num arquivo ".csv"
        df_spotify.to_csv(csv_path, sep=";", encoding="utf-8-sig", index=False)
        # Exibe uma mensagem de sucesso e exibe o local do arquivo gerado
        print("\nO arquivo 'artist_data.csv' foi gerado e salvo em:\n", os.path.abspath(csv_path), "\n", sep=";")
    
    # A função retorna o dataframe dos dados coletados do Spotify, com as adições que o usuário escolher (gênero, instrumental e letras)
    return df_spotify
