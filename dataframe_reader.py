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

    :param path_artist_info: Arquivo csv com as informações do artista
    :type path_artist_info: str
    :raises KeyError: Levanta um KeyError caso alguma coluna exigida não seja encontrada
    :return: Retorna um dataframe com as informações do arquivo csv caso o arquivo cumpra as exigências.
    :rtype: `pandas.core.frame.DataFrame`
    """
    try:
        dataframe = pd.read_csv(path_artist_info, sep = ";", encoding = "unicode_escape")
        required_columns = ["Album Name", "Track Name" , "Popularity", "Duration" , "Track Lyrics","Explicit","Genre"] # Colunas necessárias para a análise 
        for column in required_columns:
            if column not in dataframe.columns:
                raise KeyError(f"O dataframe não todas as colunas necessárias: a coluna {column} não está presente.") # Levanta um erro e fecha o programa caso o arquivo não possua alguma das colunas necessárias.
                sys.exit(0)
    except FileNotFoundError as error: # Caso o arquivo não seja encontrado, retorna uma mensagem e o erro para o usuário e fecha o programa.
        print("Arquivo não encontrado:", error)
        sys.exit(0)
    else: 
        return dataframe # Caso tudo funcione, retorna um dataframe
