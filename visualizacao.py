# Visualização
import Analise_exploratoria as ae
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image

sns.set_theme()

def most_listened_plot(dataframe):
    data = ae.most_listened(dataframe)
    sns.barplot(data=data, x="Popularidade", y=data.index.get_level_values(1))
    plt.show()

def least_listened_plot(dataframe):
    data = ae.least_listened(dataframe)
    sns.barplot(data=data, x="Popularidade", y=data.index.get_level_values(1))
    plt.show()
    
def longest_plot(dataframe):
    data = ae.longest(dataframe)
    sns.barplot(data=data, x="Duração", y=data.index.get_level_values(1))
    plt.show()  
    
def shortest_plot(dataframe):
    data = ae.shortest(dataframe)
    sns.barplot(data=data, x="Duração", y=data.index.get_level_values(1))
    plt.show()

