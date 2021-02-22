""" Helper functions for WhatsApp Analytics
"""

import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
from datetime import datetime
from collections import Counter

from wordcloud import WordCloud, STOPWORDS
import re
import emoji
import spacy

import nltk
from nltk.tokenize import word_tokenize 

def import_data(chat_text_file):
    """ Imports chat file.

    Parameters
    ----------
    chat_text_file : str
        Name of text file in /chats

    Returns
    -------
    df
        Pandas dataframe of chat

    """

    with open(chat_text_file,"r",encoding="utf-8") as textfile:
        chat = textfile.readlines()[1:]

    chat_list = create_chat_list(chat)
    df = create_dataframe_out_of_chat(chat_list)
    df = df.reset_index(drop=True)

    return df

def map_datetime(datetime, type):
    """ Maps datetime to month or weekday string
    """
    if type == "week":
        DICT = {1:"Mon",
                    2:"Tue",
                    3:"Wed",
                    4:"Thr", 
                    5:"Fri",
                    6:"Sat",
                    0:"Sun"}
    elif type == "month":
        DICT = {1:"Jan",
                    2:"Feb",
                    3:"Mar",
                    4:"Apr", 
                    5:"May",
                    6:"Jun",
                    7:"Jul",
                    8:"Aug",
                    9:"Sep",
                    10:"Oct",
                    11:"Nov",
                    12:"Dec"}
    
    return datetime.map(DICT)


def create_chat_list(chat):
    """ Creates a list with every text message that has a new timestamp as entries.

    Parameters
    ----------
    chat : list
        List of all lines of chat file

    Returns
    -------
    chat_list
        List of cleaned chat. (One line is a message per timestamp)
        
    """
    new_line_Regex = re.compile(r"\d\d.\d\d.\d\d\, \d\d:\d\d - ") 
    chat_list = []
    for index, message in enumerate(chat):
        new_message_line = new_line_Regex.search(message)
        if new_message_line:
            # Line is a new message
            chat_list.append(message.rstrip("\n"))
        else:
            # Line is not a new message
            chat_list[-1] = chat_list[-1].rstrip("\n") +" " + message.rstrip("\n")

    return chat_list

def create_dataframe_out_of_chat(chat_list):
    """Create a dataframe out of chat_list.
    """
    df = pd.DataFrame(index=None, columns=["RAW", 
                                            "date",
                                            "time", 
                                            "person", 
                                            "message", 
                                            "date_time", 
                                            "weekday", 
                                            "month", 
                                            "year", 
                                            "hour"])
    df["RAW"] = chat_list

    df["RAW"].str.rsplit(",")[0]

    for index, row in df.iterrows():
        raw = row["RAW"]
        # Check if full pattern matches
        try:
            raw.split(", ",1)[1].split(" - ",1)[1].split(": ",1)[1]
            pass
        except:
            continue
        
        # Split according to pattern
        date = row["RAW"].split(", ",1)[0]
        time = row["RAW"].split(", ",1)[1].split(" - ",1)[0]
        person = row["RAW"].split(", ",1)[1].split(" - ",1)[1].split(": ",1)[0]
        message = row["RAW"].split(", ",1)[1].split(" - ",1)[1].split(": ",1)[1]

        # Check if message was media
        if message == "<Medien ausgeschlossen>":
            continue
        
        # Fill in row in dataframe
        row["person"] = person
        row["message"] = message
        row["date_time"] = pd.to_datetime(date + " " + time,format = "%d.%m.%y %H:%M" )
        row["date"] = row["date_time"].date()
        row["time"] = row["date_time"].time()
        row["weekday"] = row["date_time"].weekday()
        row["month"] = row["date_time"].month
        row["year"] = row["date_time"].year
        row["hour"] = row["date_time"].hour 

    # create text length
    df["text_length"] = df["message"].str.len()

    # Return only rows that have been filled
    return df.dropna()         

def get_emojis(str):
    """ Filter emojis out of string.
    """
    x = [":medium-dark_skin_tone:",
            ":medium_skin_tone:",
            ":medium-light_skin_tone:",
            ":light_skin_tone:",
            ":dark_skin_tone:",
            ":male_sign:",
            ":female_sign:"]

    emoji_list = [i[0] for i in str if ((i in emoji.UNICODE_EMOJI["en"]) and (emoji.demojize(i) not in x))]
    
    return emoji_list


def count_emojis_by_name(df):
    """ Count_emojis_by_name
    """
    all_emojies = {}
    persons = df["person"].unique()

    for person in persons:
        all_emojies[person] = df[df["person"] == person]["emojis"].sum()

    df_emojies = pd.DataFrame([Counter(all_emojies[person]) for person in persons],index = persons).transpose().fillna(0)

    df_emojies.reset_index(level=0, inplace=True)
    df_emojies = pd.melt(df_emojies, id_vars=["index"],value_name='count')
    df_emojies = df_emojies.sort_values(by=["count","variable"], ascending=False)
    df_emojies.set_index(["index"], drop=True)
    df_emojies = df_emojies.rename(columns={"index": "emoji"})
    df_emojies = df_emojies.rename(columns={"variable": "person"})

    return df_emojies


def preprocess_text(text, lower=True):
    """ Prepsocess text.
    """
    text = text.replace("ä", "äe").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    # Remove punctuations and numbers
    text = re.sub("[^a-zA-Z]+", " ", text)
    # Single character removal
    text = re.sub(r"\b[a-zA-Z]\b", "", text)
    # Removing multiple spaces
    text = re.sub(r"\s+", " ", text)
    
    if lower==True:
        text = text.lower()
    
    return text

def remove_stopwords(text):
    """ Remove stopwords from text.
    """
    stop_words = nltk.corpus.stopwords.words("german")
    stop_words.extend(["ja","wa",":)",":D","hsa", "utm"])

    word_tokens = word_tokenize(text)
    filtered_word_tokens = [w for w in word_tokens if not w in stop_words]
    
    return " ".join(filtered_word_tokens)

def lemmatize_text(text):
    """ Lemmatize a text.
    """
    nlp = spacy.load("de_core_news_sm")
    word_tokens = nlp(text)

    word_tokens_lemmatized = [w.lemma_ for w in word_tokens]

    return " ".join(word_tokens_lemmatized)

def compute_wait_time(df):
    """ Computes wait times until the persons reply.
    """
    df = df[["person","date_time"]]

    df["wait_time"] = ""
    df["to_drop"] = ""
    for index, row in df.iterrows():
        if index > 1 :
            df["wait_time"][index] = df["date_time"][index] - df["date_time"][index-1]

            # Check messages that are in a row by the same person
            if df["person"][index] == df["person"][index-1]:
                df["to_drop"][index] = 1
            else:
                df["to_drop"][index] = 0
            
            # Check whether a message has been send after sleeping (we do not consider that waiting time)
            if ((df["date_time"][index].day > df["date_time"][index-1].day 
                and df["date_time"][index].hour > 5) or 
                (df["wait_time"][index].seconds / 3600 > 6)):

                df["wait_time"][index] = np.nan
            else:
                df["wait_time"][index] = int(df["wait_time"][index].seconds / 60)
    
    # Drop messages that are in a row by the same person
    df = df[df["to_drop"] == 0]
    df = df.drop(["to_drop"], axis=1)

    # Convert to numeric bc of pandas bug in groupby.mean()
    df['wait_time'] = pd.to_numeric(df['wait_time'])

    return df