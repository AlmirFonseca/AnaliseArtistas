import json
import re

import numpy as np
import pandas as pd

from lyricsgenius import Genius

# Armazena o token de acesso, obtido através da plataforma Genius
access_token = "u2SqMOrCtzWwY9xGxI6PiLn5aVqnhzWMiaMWB2BmrfuvJQL-Z_nQ4pv8gJej4isU"

# Instancia o objeto principal da API do Genius
genius = Genius(access_token, timeout=60, retries=10)