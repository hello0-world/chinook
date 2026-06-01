import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
from sqlalchemy import create_engine
import streamlit as slt
chinook_Database_URL= f"postgresql://readonly_student.tyxjmbptftftcqgozyfc:StudentRead123!@aws-1-us-east-1.pooler.supabase.com:6543/postgres"
engine = create_engine(chinook_Database_URL)

chinook_df = pd.read_sql_query(
           """
            select 
                t."name" as track_name,
                t.album_id ,
                a.title AS album_title,
                at."name" AS artist_name,
                g."name" AS genre_name,
                mt."name" AS media_name,
                t.bytes ,
                t.composer ,
                t.genre_id ,
                t.media_type_id ,
                t.milliseconds ,
                t.track_id ,
                t.unit_price
            from track t  
            inner join album a 
                on a.album_id = t.album_id 
            inner join genre g  
                on g.genre_id = t.genre_id 
            inner join media_type mt 
                on mt.media_type_id = t.media_type_id 
            inner join artist at 
                    on at.artist_id = a.artist_id 
            """,engine
)

artist = slt.selectbox('Selec an Artist', chinook_df['artist_name'].unique())
filter_artist_df = chinook_df[chinook_df['artist_name'] == artist ]
track_count_by_genre = (
        filter_artist_df
        .groupby('genre_name')
        .agg(num_tracks=('track_id' , 'count'))
        .sort_values(by='num_tracks',ascending=False)
        .reset_index()
    )
fig, ax = plt.subplots()
sns.barplot(
    data=track_count_by_genre,
    x='num_tracks',
    y='genre_name',
    palette='Set2',
    ax= ax
)
slt.pyplot(fig)
#slt.dataframe(track_count_by_genre)
slt.dataframe(filter_artist_df[['track_name','genre_name' , 'album_title' ,'artist_name' ]])