"""

A biblioteca lyricsgenius utiliza a API da Genius para acessar dados de artistas, álbuns e músicas e,
para obter as letras das músicas, realiza um scrapping na página de cada música.

Porém, por motivos de ausência de atualizações no módulo lyricsgenius, o scrapping é realizado sobre a <div> errada.

Dessa forma, o resultado obtido da aquisição das letras é obtido com 2 erros:
    - "{nome da musica} Lyrics", no topo de cada letra
    - "{numero de likes}Embed", no final de cada letra

Para solucionar esse problema, esse script encontra o arquivo que contém a função responsável
por realizar o scrapping das letras e altera o padrão RegEx que indica a <div> que contém as letras,
apontando para a <div> correta e, consequentemente, solucionando os erros ligados à esse padrão incorreto

"""

import os

import lyricsgenius
import re

# Obtém o path do arquivo genius.py, do módulo lyricsgenius
lyricsgenius_init_path = lyricsgenius.__file__
lyricsgenius_root_path = os.path.dirname(lyricsgenius_init_path)
lyricsgenius_genius_path = os.path.join(lyricsgenius_root_path, "genius.py")

# Checa se o caminho encotrado é válido
if os.path.exists(lyricsgenius_genius_path):    
    try:
        # Inicia uma variável para armazenar o conteúdo do arquivo
        genius_file_content = ""

        # Abre o arquivo que contém o erro no modo de leitura e armazena o conteúdo na variável criada
        with open(lyricsgenius_genius_path, "r", encoding='utf-8') as genius_read_file:
            genius_file_content = genius_read_file.read()
            genius_read_file.close()
            
        # Busca pelos termos corretos e incorretos, a fim de tentar reconhecer se o erro já foi corrigido
        search_for_incorret_class = re.search("Lyrics__Root", genius_file_content)
        search_for_corret_class = re.search("Lyrics__Container", genius_file_content)
        
        if search_for_corret_class == None and search_for_incorret_class == None:
            raise Exception("O erro não foi encontrado. Portanto, não foi possível solucioná-lo")
        
        if search_for_corret_class != None and search_for_incorret_class == None:
            raise Exception("O erro já foi solucionado.")
            
        # Substitui "Lyrics__Root" por "Lyrics__Container" na string do conteúdo do arquivo, utilizando RegEx
        genius_file_content = re.sub("Lyrics__Root", "Lyrics__Container", genius_file_content)
        
        # Busca pelos termos corretos e incorretos, visando verificar se o erro não foi corrigido como esperado
        search_for_incorret_class = re.search("Lyrics__Root", genius_file_content)
        search_for_corret_class = re.search("Lyrics__Container", genius_file_content)
            
        if search_for_corret_class == None and search_for_incorret_class != None:
            raise Exception("O erro presente no módulo 'lyricsgenius' não pôde ser corrigido")

        # Abre o arquivo que contém o erro no modo de escrita e o sobrescreve com o conteúdo já corrigido
        with open(lyricsgenius_genius_path, "w", encoding="utf-8") as genius_write_file:    
            genius_write_file.write(genius_file_content)
            genius_write_file.close()
    
    # Caso ocorra algum erro
    except Exception as error:
        print("Não foi possível realizar a operação pois ocorreu um erro:", error)
    
    # Caso não ocorra nenhum erro durante o processo
    else:
        print("O erro foi encontrado e foi corrigido com sucesso!")
  
# Caso não foi possível encontrar o caminho do arquivo que contém o erro a ser corrigido
else:
    print("O arquivo 'genius.py' não foi localizado.\nNão foi possível corrigir o erro no módulo 'lyricsgenius'")
