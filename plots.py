""" Plot functions for WhatsApp Analytics
author: Jonas Rauch
"""

from matplotlib import pyplot as plt 
import seaborn as sns
from src import *
import calendar
import streamlit as st

class plots:
    """
    A class to create plots.

    ...

    Attributes
    ----------
    data : pandas.Series
        Data to plot. Series only contains index and values.
    title : str
        Title of the plot
    """

    def __init__(self, data=None, title=None, x=None, y=None, hue=None):
        self.data = data
        self.title = title
        self.x = x
        self.y = y
        self.hue = hue
    
class word_clouds_plot(plots):
    def plot(self, figsize=(30,8), title_size=32):
        fig = plt.figure(figsize=figsize)
        fig.suptitle(self.title, fontsize=title_size)
        persons = self.data["person"].unique()

        n_rows = int(np.ceil(len(persons) / 2))
        n_cols = 2


        for person, index in zip(persons, range(len(persons))):
            text = self.data[self.data["person"]==person]["message"].sum()
            text = remove_stopwords(text)
            text = lemmatize_text(text)
            text = preprocess_text(text)
            wordcloud = WordCloud(height=600, width=600,
                            background_color='white', 
                            min_font_size=20,
                            max_words=50).generate(text) 

            plt.subplot(n_rows, n_cols ,index+1)
            plt.imshow(wordcloud, interpolation="bilinear") 
            plt.title(person, fontsize=24)
            plt.axis('off')
            
        return fig
        