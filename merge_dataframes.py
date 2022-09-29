import numpy as np
import pandas as pd

def filter_albums(albums, filter_terms, case_sensitive=False, reverse=False):
    filter_terms_list = filter_terms.split(",")
    for term_index, term in enumerate(filter_terms_list):
        filter_terms_list[term_index] = term.strip()
    
    mask = np.zeros(albums.shape[0], dtype=bool)
    
    for term in filter_terms_list:
        mask = mask | albums.str.contains(term, case=case_sensitive)
        
    if reverse:
        mask = ~mask
    
    return albums[~mask]

df = pd.read_csv("Letras - Coldplay.csv", encoding="ISO-8859-1", sep=";")

df_filter = filter_albums(df["album_name"], "  live,remix ,edition,radio,session, version")

print(df_filter.unique())