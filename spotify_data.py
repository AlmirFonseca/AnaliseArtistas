import spotipy #pip install spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import time

# Define as credenciais para o uso da API
# client_id = "6a1edef9875b4c79a81e70db08f91c79"
# client_secret = "bd17a1c083284bd4882f1c0839a6df65"

# Função de Autenticação
def autentication(client_id, client_secret):
    credentials = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
    return credentials

#client_credentials_manager = autentication(client_id, client_secret)
#print(client_credentials_manager)
