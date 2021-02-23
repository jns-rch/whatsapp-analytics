''' Streamlit GUI for plots
Currently, there is only a rough version available
to show the principle. Much work to do on make it more 
interactive and beautiful.
'''

import streamlit as st
import numpy as np
import pandas as pd
import glob 
import os
import argparse

# Own imports
from src import *
from plotly_plots import Plotter

# Get folder via user input
@st.cache
def get_folder():
    return input("Folder: ")
FOLDER = get_folder()

# Title
st.title("WhatsApp Chat Analysis")
myFiles = glob.glob(f"{FOLDER}/*.txt")
myFiles = [f.replace(FOLDER+"\\", "") for f in list(myFiles)]
CHAT_TEXT_FILE = st.sidebar.selectbox(label="Select chat", options=myFiles, index=0)

# Chat file selection
@st.cache(allow_output_mutation=True)
def import_data_to_streamlit(file):
    df = import_data(file)
    return df

# DataFrame
df = import_data_to_streamlit(os.path.join(FOLDER, CHAT_TEXT_FILE))
# Get unique persons
persons = df["person"].unique()
PERSON = st.sidebar.selectbox(label="Select person", options=persons, index=0)

# Create Plotter object
P = Plotter()

# Messages per person
plot_data = pd.DataFrame()
plot_data["messages_per_person"]=df.groupby(['person']).count()["message"]
plot_data.reset_index(inplace=True)
plot_data = plot_data.sort_values(by=["person"])
messages_pie = P.pieplot(data=plot_data, 
                    values="messages_per_person", 
                    names="person",
                    color="person",
                    title_text="Messages per person")
st.plotly_chart(messages_pie, use_container_width=True)

# Text length per person
plot_data = df[df["text_length"]<=200][["text_length","person"]]
plot_data = plot_data.sort_values(by=["person"])
text_length_bar = P.histogram(data=plot_data, 
                    x="text_length", 
                    color=plot_data["person"], 
                    title_text="Text length per person", 
                    xaxis_title="Text length [characters]", 
                    yaxis_title="Count")
st.plotly_chart(text_length_bar, use_container_width=True)

# Messages timeline
messages_per_date =  pd.DataFrame(df.groupby(['date']).count()['message'])
r = pd.date_range(start=messages_per_date.index.min(), end=messages_per_date.index.max())
plot_data = pd.DataFrame()
plot_data = messages_per_date.reindex(r).fillna(0).rename_axis('date').reset_index()
time_line = P.lineplot(data=plot_data, 
                    x="date",
                    y="message", 
                    title_text="Messages per date", 
                    xaxis_title="Date", 
                    yaxis_title="Messages")
st.plotly_chart(time_line, use_container_width=True)

# Emojis
df["emojis"] = ""
df["emojis"] = df['message'].apply(lambda x: get_emojis(x))
df_emojies = count_emojis_by_name(df)
plot_data = df_emojies[df_emojies["count"] >= 5]
plot_data = plot_data.sort_values(by=["person"])
emoji_bar = P.barplot(data=plot_data, 
                    x="emoji", 
                    y="count", 
                    color="person", 
                    barmode="group", 
                    title_text="Emojies used by person", 
                    xaxis_title="Emojies", 
                    yaxis_title="Count",
                    xtickangle=0)
st.plotly_chart(emoji_bar, use_container_width=True)

st.title('Analysis corresponding to specific person')

# Messages per hour
plot_data = pd.DataFrame()
df_temp = df[df["person"] == PERSON]
plot_data["messages_per_hour_per_person"] = df_temp.groupby(['hour']).count()['message'] / len(df_temp.groupby(['hour']).count().index)
plot_data.reset_index(inplace=True)
messages_per_hour_bar = P.barplot(data=plot_data, 
                    x="hour",
                    y="messages_per_hour_per_person",
                    title_text="Average messages per hour for " + PERSON, 
                    xaxis_title="Hour of the day", 
                    yaxis_title="Messages",
                    xtickvals=plot_data["hour"])
st.plotly_chart(messages_per_hour_bar, use_container_width=True)