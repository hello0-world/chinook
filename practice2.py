import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USERNAME')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

query = """ YOUR QUERY HERE """

@st.cache_data
def load_data():
    return pd.read_sql(query, engine)

df = load_data()

df['minutes'] = df['milliseconds'] / 60000

selected_genre = st.multiselect(
    'Select the genre',
    df['genre_name'].unique(),
    default=list(df['genre_name'].unique())
)

filtered_df = df[df['genre_name'].isin(selected_genre)]

# Genre plot
track_count_by_genre = (
    filtered_df.groupby('genre_name')
    .agg(num_tracks=('track_id', 'count'))
    .reset_index()
)

fig, ax = plt.subplots()
sns.barplot(
    data=track_count_by_genre.sort_values('num_tracks', ascending=False),
    y='genre_name',
    x='num_tracks',
    ax=ax,
    legend=False
)
st.pyplot(fig)

# Artist plot
track_count_by_artist = (
    filtered_df.groupby('artist_name')
    .agg(num_tracks=('track_id', 'count'))
    .reset_index()
)

fig1, ax1 = plt.subplots()
sns.barplot(
    data=track_count_by_artist.sort_values('num_tracks', ascending=False).head(25),
    y='artist_name',
    x='num_tracks',
    ax=ax1,
    legend=False
)
st.pyplot(fig1)

# Histogram
fig2, ax2 = plt.subplots()
sns.histplot(data=filtered_df, x='minutes', bins=30, ax=ax2)
st.pyplot(fig2)