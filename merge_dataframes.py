import numpy as np
import pandas as pd

# TODO Remover "duplicatas"
# TODO Ordem alfabética
# TODO Número de tracks

# Filtra o dataframe, excluindo as entradas que possuem algum dos termos na coluna indicada
def filter_dataframe(dataframe, dataframe_column, filter_terms, case_sensitive=False, reverse=False):
    
    # Gera uma lista de termos a partir do split da string recebida
    filter_terms_list = filter_terms.split(",")
    
    # Realiza um .strip() em cada termo, a fim de excluir espaços em branco desnecessários
    for term_index, term in enumerate(filter_terms_list):
        filter_terms_list[term_index] = term.strip()
    
    # Gera uma máscara "virgem", repleta de "False"
    mask = np.zeros(dataframe.shape[0], dtype=bool)
    
    # Itera sobre os termos, acumulando as máscaras geradas
    for term in filter_terms_list:
        mask = mask | dataframe[dataframe_column].str.contains(term, case=case_sensitive)
        
    # Caso o usuário deseje, a máscara é invertida
    if reverse:
        mask = ~mask
    
    # A função retorna o dataframe com a máscara aplicada
    return dataframe[~mask]

# Lê o arquivo csv de letras geradas a partir da API da Genius e o converte num dataframe
genius_dataframe = pd.read_csv("Letras - Coldplay.csv", encoding="ISO-8859-1", sep=";")

# Aplica o filtro sobre o genius_dataframe, removendo álbuns que possuam, em seus títulos, termos como "live", "remix"...
genius_dataframe = filter_dataframe(genius_dataframe, "album_name", "  live,remix ,edition, deluxe,radio,session, version")

# Exibe o dataframe após a aplicação do filtro
print(genius_dataframe)