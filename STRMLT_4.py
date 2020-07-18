# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 20:48:16 2020

@author: shivj
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64
import seaborn as sns
from PIL import Image


image=Image.open(r"numpy_altered.jpg")
st.image(image, format="JPEG", use_column_width=True)

st.title("NBA Player Stats Exploration")
st.markdown("""
            This app scrapes data and performs exploratory data analysis on it
            * **Data Source:** [Basketball-reference.com](https://www.basketball-reference.com/).
            """)
            
st.sidebar.header("Input Features")

#create a range of years for basketball data and reverse it for UI purposes
selected_year=st.sidebar.selectbox("Year", list(reversed(range(1984, 2020))))

#WebScraping of NBA Stats
@st.cache
def load_data(year):
    url="https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html=pd.read_html(url, header=0)
    df=html[0]
    raw=df.drop(df[df.Age=='Age'].index)
    raw=raw.fillna(0)
    playerstats=raw.drop(['Rk'], axis=1)
    return playerstats

playerstats=load_data(selected_year)

#Side_bar Team selection
sorted_unique_team=sorted(playerstats.Tm.unique())
selected_team=st.sidebar.multiselect("Team",sorted_unique_team, sorted_unique_team[:3])

#sidebar position selection
unique_pos=["C", "PF", "SF", "PG", "SG"]
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos[:1])

df_selected_teams=playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header("Display Player Stats of Selected Team(s)")
st.dataframe(df_selected_teams)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_teams), unsafe_allow_html=True)

col=list(df_selected_teams.columns)
column_names=col[4:]
selected_metric=st.sidebar.selectbox("Select a metric for a Bargraph", column_names)

st.markdown("""
                
         * **Click on the buttons bellow for graphs**
         
         """)

if st.button("Intercorrelation Heatmap"):
    st.header("Intercorrelation Matrix Heatmap")
    df_selected_teams.to_csv("output.csv")
    df=pd.read_csv("output.csv")
    
    corr=df.corr()
    plt.subplots(figsize=(20,20))
    sns.heatmap(corr, annot=True, square=True, cmap='Blues')
    st.pyplot()
    
if st.button("BarGraph"):
    st.header("Bargraph")
    df_selected_teams.to_csv("output.csv")
    df=pd.read_csv("output.csv")
    plt.subplots(figsize=(20,20))
    sns.barplot(x=df["Player"], y=df[selected_metric], data=df)
    st.pyplot()