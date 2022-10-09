from modules import artist_dataframe_generator as adg

# Define as credenciais para o uso da API do Spotify
sp_client_id = "6a1edef9875b4c79a81e70db08f91c79"
sp_client_secret = "bd17a1c083284bd4882f1c0839a6df65"

# Define a credencial para o uso da API da Genius
ge_access_token = "u2SqMOrCtzWwY9xGxI6PiLn5aVqnhzWMiaMWB2BmrfuvJQL-Z_nQ4pv8gJej4isU"

# Define o nome do artista a ser analisado
artist_name = "Coldplay"

# Imprime uma mensagem inicial
print("\u001b[32;1m{}\033[m".format(f"\nIniciando a geração de base de dados do {artist_name}..."))

try:
    # Gera e salva num arquivo ".csv" um dataframe contendo os dados do artista, seus álbuns e suas faixas
    coldplay_data = adg.generate_dataframe_of(artist_name, sp_client_id, sp_client_secret, ge_access_token, filter_terms="", save_csv=True)
    
# Recebe as exceções e as exibe de maneira amigável ao usuário 
except BaseException as error:
    print("\u001b[34;1m{}\033[m".format("=-"*60))
    print("Ocorreu um erro durante o execução do projeto:\n", error.__class__.__name__, "\n", error)
# Caso nenhuma exceção ocorra durante a execução
else:
    print("\u001b[34;1m{}\033[m".format("=-"*60))
    print("\u001b[32;1m{}\033[m".format("A execução foi concluída com sucesso!"))
# Exibe uma mensagem ao final da execução
finally:
    print("\u001b[34;1m{}\033[m".format("=-"*60))
    print("\nEncerrando a aplicação...")