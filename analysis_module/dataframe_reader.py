""" Módulo de leitura do csv e criação do dataframe
Nesse módulo estão contidas as funções que validam arquivos csv garantindo que eles contenham todas as informações para a ánalise de dados, caso eles estejam de acordo com o estabelecido, é criado um dataframe no formato exigido.
"""

# Importe as bibliotecas necessárias
import sys
import pandas as pd
import numpy as np


# Função que checa se um csv contém as informações necessárias para a análise de dados e retorna um dataframe caso ele contenha.
def is_valid(path_artist_info):
    """Essa função checa se o caminho fornecido para um arquivo csv é válido e se esse arquivo possui todas as colunas necessárias para a análise de dados. Caso todos os requisitos sejam atendidos, a função retorna um dataframe com as informações do arquivo
    
    :param path_artist_info: Arquivo ``.csv`` com as informações do artista
    :type path_artist_info: `str`
    :raises KeyError: Levanta um ``KeyError`` caso alguma coluna exigida não seja encontrada
    :return: Retorna um dataframe com as informações do arquivo .csv caso o arquivo cumpra as exigências.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    try:
        dataframe = pd.read_csv(path_artist_info, sep = ";", encoding = "utf-8")
        if dataframe.empty:
            raise Exception("O dataframe está vazio.") 
            sys.exit(0)
        required_columns = ["Album Name", "Track Name" , "Popularity", "Duration" , "Track Lyrics","Explicit","Genre"] # Colunas necessárias para a análise 
        for column in required_columns:
            if column not in dataframe.columns:
                raise KeyError(f"O dataframe não todas as colunas necessárias: a coluna {column} não está presente.") # Levanta um erro e fecha o programa caso o arquivo não possua alguma das colunas necessárias.
                sys.exit(0)
    except FileNotFoundError as error: # Caso o arquivo não seja encontrado, retorna uma mensagem e o erro para o usuário e fecha o programa.
        print("Arquivo não encontrado:", error)
        sys.exit(0)
    except ValueError as error:# Caso o arquivo não seja uma string, retorna uma mensagem e o erro para o usuário e fecha o programa.
        print("Tipo inserido inválido:", error)
        sys.exit(0)
    else: 
        return dataframe # Caso tudo funcione, retorna um dataframe



# Recebe um dataframe com informações gerais do artista e um arquivo csv com os álbuns premiados e seus respectivos prêmios e retorna um dataframe com essas informações agrupadas.
def add_awards(original_dataframe,path_album_awards):
    """ Recebe um dataframe com todas as colunas necessárias para a análise e recebe o caminho para um arquivo csv com duas colunas: ``Album Name`` e ``Awards``, que contém os álbuns premiados e seus respectivos prêmios.
    
    :param original_dataframe: Dataframe com colunas necessárias para a análise exploratória
    :type original_dataframe: `pandas.core.frame.DataFrame`
    :param path_album_awards: Arquivo ``.csv`` com os álbuns e seus prêmios.
    :type path_album_awards: `str`
    :return: Dataframe com as informações do primeiro parâmetro da função acrescido de uma coluna ``Awards`` com os prêmios dos álbuns.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    try:
        album_awards_dataframe = pd.read_csv(path_album_awards, sep = ";",encoding = "unicode_escape") 
        grouped_dataframe = original_dataframe.groupby(level=0) # Agrupa o "original_dataframe" pelo índice de nível zero, não resulta em nenhuma mudança significativa mas é útil nas linhas subsequentes.
        result_dataframe = pd.DataFrame() #Crie um dataframe vazio onde serão armazenados os resultados.
        for index, selected_dataframe in grouped_dataframe: # A variável selected_dataframe armazena um dataframe composto por uma linha do "original_dataframe"
            album = selected_dataframe["Album Name"].values
            if album in album_awards_dataframe["Album Name"].values:
                mask = album_awards_dataframe["Album Name"] == album[0] # Verifica se o álbum de selected_dataframe está entre os álbuns premiados
                selected_dataframe["Awards"] = album_awards_dataframe[mask]["Awards"].values # Caso esteja, atribui os dados dos prêmios
                result_dataframe = pd.concat((result_dataframe,selected_dataframe), axis=0) # Adiciona a linha ao dataframe vazio
            else:
                selected_dataframe["Awards"] = ""
                result_dataframe = pd.concat((result_dataframe,selected_dataframe), axis=0)
    except FileNotFoundError as error: #Levanta um erro e sai do programa caso o código não seja encontrado
        print("O arquivo não foi encontrado:",error)
        sys.exit(0)
    except KeyError as error: #Levanta um erro e sai do programa caso uma das colunas exigidas não exista
        print("O arquivo não possui todas as colunas pedidas:",error)
        sys.exit(0)
    except AttributeError as error: #Levanta um erro e sai do programa caso o parâmetro passado não seja o correto
        print("Um dos arquivos não possui o formato exigido:",error)
        sys.exit(0)
    except ValueError as error:# Caso o segundo parâmetro não seja uma string, retorna uma mensagem e o erro para o usuário e fecha o programa.
        print("Tipo inserido inválido:", error)
        sys.exit(0)
    else:
        return result_dataframe


# Converte um objeto no formato "mm:ss" e o transforma para tempo em segundos.    
def time_to_seconds(object):
    """Essa função converte um objeto no formato ``mm:ss`` e o transforma para tempo em segundos.    
    
    :param object: Objeto presente em uma coluna dataframe formatado como ``mm:ss`` que representa a duração da música
    :type object: object (pandas)
    :return: Objeto convertido para `int`, representando a duração da música em segundos.
    :rtype: `int`
    
    """
    separated = str(object).split(":")
    try:
        seconds = int(separated[0])*60 + int(separated[1])
    except TypeError as error:
        print("A duração não está no formato exigido",error)
        sys.exit(0)
    return seconds

# Recebe um dataframe e o retorna com multi index no modelo exigido e com uma coluna representando a duração da música em segundos.
def create_final_dataframe(dataframe):
    """Modifica um dataframe para que ele possua um multi index a partir das colunas pedidas: ``Album Name`` e ``Track Name`` e para que exista uma nova coluna chamada ``Duration Seconds``.
    
    :param dataframe: Dataframe com todas as informações necessárias e sem multi index
    :type dataframe: `pandas.core.frame.DataFrame`
    :return: Dataframe com todas as informações do dataframe utilizado como parâmetro da função e com multi index composto por: ``Album Name`` e ``Track Name``, respectivamente. Também adiciona a coluna ``Duration Seconds``.
    :rtype: `pandas.core.frame.DataFrame`
    
    """
    try:
        dataframe["Duration Seconds"] = dataframe["Duration"].apply(lambda d: time_to_seconds(d))  # Cria a coluna "Duration Seconds"
        multi_indices = pd.MultiIndex.from_arrays([dataframe["Album Name"],dataframe["Track Name"]],names=("Album Name","Track Name")) #Cria o multi index
        dataframe.set_index(multi_indices,inplace=True) #Adiciona o multi index ao dataframe
        dataframe.drop(columns="Album Name",inplace = True) #Remove as colunas antigas que tornaram-se index
        dataframe.drop(columns="Track Name",inplace = True)
    except TypeError as error: # Levanta uma exceção e sai do programa caso o parâmetro não seja um dataframe
        print("A variável não é um dataframe: ", error)
        sys.exit(0)
    except KeyError as error: # Levanta uma exceção e sai do programa caso oo dataframe não possua uma das colunas pedidas
        print("O dataframe não possui uma das colunas necessárias: ", error)
        sys.exit(0)
    else:
        return dataframe
    
