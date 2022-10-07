from modules import artist_dataframe_generator as adg

# Define as credenciais para o uso da API do Spotify
sp_client_id = "6a1edef9875b4c79a81e70db08f91c79"
sp_client_secret = "bd17a1c083284bd4882f1c0839a6df65"

# Define a credencial para o uso da API da Genius
ge_access_token = "u2SqMOrCtzWwY9xGxI6PiLn5aVqnhzWMiaMWB2BmrfuvJQL-Z_nQ4pv8gJej4isU"

# Define o nome do artista a ser analisado
artist_name = "Coldplay"

# Gera e salva num arquivo ".csv" um dataframe contendo os dados do artista, seus álbuns e suas faixas
coldplay_data = adg.generate_dataframe_of(artist_name, sp_client_id, sp_client_secret, ge_access_token, filter_terms="", save_csv=True, append_genre=False)
