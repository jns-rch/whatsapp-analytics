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

# Own imports
from src import *
from plotly_plots import Plotter

# ADD FOLDER HERE
# AS THERE IS NO PERFECT FILE INPUT FOR STREAMLIT
FOLDER = "C:/Users/jonas/Documents/Dokumente/Projekte/00_DATA/chats"

# Titel
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
plt_data = pd.DataFrame()
plt_data["messages_per_person"]=df.groupby(['person']).count()["message"]
plt_data.reset_index(inplace=True)
x=plt_data["messages_per_person"]
y=plt_data["person"]
pie0 = P.pieplot(data=plt_data, 
                    values="messages_per_person", 
                    names="person",
                    title_text="Messages per person")
st.plotly_chart(pie0, use_container_width=True)

# Text length per person
data = df[df["text_length"]<=200][["text_length","person"]]
bar0 = P.histogram(data=data, 
                    x="text_length", 
                    color=data["person"], 
                    title_text="Text length per person", 
                    xaxis_title="Text length [characters]", 
                    yaxis_title="Count")
st.plotly_chart(bar0, use_container_width=True)

# Messages timeline
messages_per_date =  pd.DataFrame(df.groupby(['date']).count()['message'])
r = pd.date_range(start=messages_per_date.index.min(), end=messages_per_date.index.max())
messages_count = messages_per_date.reindex(r).fillna(0).rename_axis('date').reset_index()
plot_data = messages_count
line1 = P.lineplot(data=plot_data, 
                    x="date",
                    y="message", 
                    title_text="Messages per date", 
                    xaxis_title="Date", 
                    yaxis_title="Messages")
st.plotly_chart(line1, use_container_width=True)

# Emojis
df["emojis"] = ""
df["emojis"] = df['message'].apply(lambda x: get_emojis(x))
df_emojies = count_emojis_by_name(df)
plot_data = df_emojies[df_emojies["count"] >= 5]
bar2 = P.barplot(data=plot_data, 
                    x="emoji", 
                    y="count", 
                    color="person", 
                    barmode="group", 
                    title_text="Emojies used by person", 
                    xaxis_title="Emojies", 
                    yaxis_title="Count",
                    xtickangle=0)
st.plotly_chart(bar2, use_container_width=True)

st.title('Analysis corresponding to specific person')

# Messages per hour
plot_data = pd.DataFrame()
df_temp = df[df["person"] == PERSON]
plot_data["messages_per_hour_per_person"] = df_temp.groupby(['hour']).count()['message'] / len(df_temp.groupby(['hour']).count().index)
plot_data.reset_index(inplace=True)
bar3 = P.barplot(data=plot_data, 
                    x="hour",
                    y="messages_per_hour_per_person",
                    title_text="Average messages per hour for " + PERSON, 
                    xaxis_title="Hour of the day", 
                    yaxis_title="Messages",
                    xtickvals=plot_data["hour"])
st.plotly_chart(bar3, use_container_width=True)