import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import streamlit as st
 
DATABASE_URL = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
 
query = """
    SELECT
        t."name" ,
        t.album_id ,
        a.title AS album_title,
        a2."name" AS artist_name,
        g."name" AS genre_name,
        mt."name" AS media_name,
        t.bytes ,
        t.composer ,
        t.genre_id ,
        t.media_type_id ,
        t.milliseconds ,
        t.track_id ,
        t.unit_price
       
    FROM track t
    JOIN album a
        ON t.album_id = a.album_id
    JOIN artist a2
        ON a2.artist_id = a.artist_id
    JOIN genre g
        ON g.genre_id = t.genre_id
    JOIN media_type mt
        ON mt.media_type_id = t.media_type_id"""
 
df = pd.read_sql(query, engine)
 
df['minutes'] = df['milliseconds'] / 60000
 
selected_genre = st.multiselect('Select the genre', df['genre_name'].unique(), default=df['genre_name'].unique())
 
filtered_df = df[df['genre_name'].isin(selected_genre)]
 
track_count_by_genre = filtered_df.groupby('genre_name').agg(num_tracks=('track_id', 'count')).reset_index()
print(track_count_by_genre)
 
fig,ax = plt.subplots(figsize=(10,6))
sns.barplot(data = track_count_by_genre.sort_values('num_tracks', ascending=False), y = 'genre_name', x = 'num_tracks', ax=ax)
st.pyplot(fig)
 
track_count_by_artist = filtered_df.groupby('artist_name').agg(num_tracks=('track_id', 'count')).reset_index()
print(track_count_by_artist)
 
fig1,ax1 = plt.subplots(figsize=(10,6))
 
sns.barplot(data = track_count_by_artist.sort_values('num_tracks', ascending=False).head(25), y = 'artist_name', x = 'num_tracks', ax =ax1)
st.pyplot(fig1)
 
 
fig2,ax2 = plt.subplots(figsize=(10,6))
sns.histplot(data = filtered_df, x = 'minutes', binwidth=1, ax=ax2)
st.pyplot(fig2)