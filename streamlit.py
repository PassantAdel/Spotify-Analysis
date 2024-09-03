from numpy import poly
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("/content/drive/MyDrive/dataset/Most Streamed Spotify Songs 2024.csv", 
                  encoding='unicode_escape')

st.title('Spotify Data Visualization Dashboard')

st.sidebar.image("/content/drive/MyDrive/dataset/spotify.png", use_column_width=True)


st.sidebar.title('Navigation')

visualization = st.sidebar.selectbox('Select a visualization:', [
    'Top 50 Albums by Count',
    'Top 50 Tracks by Count',
    'Top 50 Artists by Count',
    'Top 20 Ranked Artist',
    'Least 20 Ranked Artist',
    'Top 10 Most Streamed Tracks',
    'Top 10 Most Streamed Artists',
    'Top 10 Tracks by Playlist Count',
    'All Time Rank Popularity',
    'Spotify Stream Over Time',
    'Spotify Reach Vs Playlist Count'
])


def preprocessing(dataframe):
  data = dataframe.iloc[:, :11]
  data.drop_duplicates(inplace=True)
  data['Spotify Streams'] = data['Spotify Streams'].str.replace(',', '').astype(float)
  data['Spotify Playlist Count'] = data['Spotify Playlist Count'].str.replace(',', '').astype(float)
  data['Spotify Playlist Reach'] = data['Spotify Playlist Reach'].str.replace(',', '').astype(float)

  # Fill Nulls
  # Fill 'Artist' with 'Unknown Artist'
  data['Artist'].fillna('Unknown Artist', inplace=True)

  data['Track Score'].fillna(data['Track Score'].median(), inplace=True)
  data['Spotify Streams'].fillna(data['Spotify Streams'].median(), inplace=True)
  data['Spotify Playlist Count'].fillna(data['Spotify Playlist Count'].median(), inplace=True)
  data['Spotify Playlist Reach'].fillna(data['Spotify Playlist Reach'].median(), inplace=True)

  # For Spotify Popularity, depending on skewness, either the mean or median
  data['Spotify Popularity'].fillna(data['Spotify Popularity'].mean(), inplace=True)
  print("preeeeeee")
  return data

df = preprocessing(data)
print ("preprocessed")

def Top_50_Albums_by_Count():
  top_albums = df['Album Name'].value_counts().nlargest(50)

  top_albums_df = top_albums.reset_index()
  top_albums_df.columns = ['Album Name', 'Count']

  plt.figure(figsize=(20, 10))
  sns.barplot(x='Album Name', y='Count', data=top_albums_df, palette='viridis')
  plt.title('Top 50 Albums by Count', fontsize=20)
  plt.xlabel('Album Name', fontsize=12)
  plt.ylabel('Count', fontsize=12)
  plt.xticks(rotation=45, ha='right')
  st.pyplot(plt)


def top_50_tracks_by_count():
  top_tracks = df['Track'].value_counts().nlargest(50)

  top_tracks_df = top_tracks.reset_index()
  top_tracks_df.columns = ['Track', 'Count']

  plt.figure(figsize=(20, 10))
  sns.barplot(x='Track', y='Count', data=top_tracks_df, palette='viridis')
  plt.title('Top 50 Tracks by Count', fontsize=20)
  plt.xlabel('Track Name', fontsize=12)
  plt.ylabel('Count', fontsize=12)
  plt.xticks(rotation=45, ha='right')
  st.pyplot(plt)


def top_50_artists_by_count():

  top_artist = df['Artist'].value_counts().nlargest(50)
  top_artist_df = top_artist.reset_index()
  top_artist_df.columns = ['Artist', 'Count']

  plt.figure(figsize=(20, 10)) 

  sns.barplot(x='Artist', y='Count', data = top_artist_df, palette='viridis')
  plt.title('Top 50 Artists by Count', fontsize=20)
  plt.xlabel('Artist Name', fontsize=12)
  plt.ylabel('Count', fontsize=12)
  plt.xticks(rotation=45, ha='right')
  st.pyplot(plt)


def top20_ranked_artist():
  top_ranked_artist=df[['Artist','All Time Rank']]
  top_20artist = top_ranked_artist.head(20)
  plt.figure(figsize=(20, 10))

  plt.title("TOP 20 ARTIST BY RANK ON SPOTIFY", fontsize=20)
  plt.xlabel("ARTIST NAME")
  sns.barplot(x=top_20artist['Artist'],y=top_20artist['All Time Rank'],palette='viridis')
  plt.xticks(rotation=45, ha = 'right')
  st.pyplot(plt)

def least20_ranked_artist():
  top_ranked_artist=df[['Artist','All Time Rank']]
  top_20artist = top_ranked_artist.tail(20)

  plt.title("LEAST POPULAR TOP 20 ARTIST BY RANK ON SPOTIFY")
  plt.xlabel("ARTIST NAME")
  sns.barplot(x=top_20artist['Artist'],y=top_20artist['All Time Rank'],palette='viridis')
  plt.xticks(rotation=45, ha = 'right')
  st.pyplot(plt)

def top_10_most_streamed_tracks():
  top_streamed = df.sort_values(by='Spotify Streams', ascending=False).head(14)
  sns.barplot(x='Track', y='Spotify Streams', data=top_streamed, palette='Blues_d')
  plt.title('Top 10 Most Streamed Tracks', fontsize=15)
  plt.xlabel('Track', fontsize=12)
  plt.ylabel('Spotify Streams', fontsize=12)
  plt.xticks(rotation=45, ha='right')
  st.pyplot(plt)


def top_10_most_streamed_artists():
  top_streamed = df.sort_values(by='Spotify Streams', ascending=False).head(14)
  sns.barplot(x='Artist', y='Spotify Streams', data=top_streamed, palette='Blues_d')
  plt.title('Top 10 Most Streamed Artist', fontsize=15)
  plt.xlabel('Track', fontsize=12)
  plt.ylabel('Spotify Streams', fontsize=12)
  plt.xticks(rotation=45, ha='right')
  st.pyplot(plt)

def top_10tracks_by_playlist_count():
  top_tracks_playlist = df.sort_values(by='Spotify Playlist Count', ascending=False).head(10)
  sns.barplot(x='Track', y='Spotify Playlist Count', data=top_tracks_playlist, palette='coolwarm')
  plt.title('Top 10 Tracks by Playlist Count')
  plt.xlabel('Track Name')
  plt.ylabel('Spotify Playlist Count')
  plt.xticks(rotation=45, ha='right')
  st.pyplot(plt)


def all_time_rank_popularity():
  sns.scatterplot(x='All Time Rank', y='Spotify Popularity', data=df)
  plt.title('Track Popularity vs. All Time Rank')
  plt.xlabel('All Time Rank')
  plt.ylabel('Spotify Popularity')
  st.pyplot(plt)

def spotify_stream_over_time():
  df['Release Date'] = pd.to_datetime(df['Release Date'])  # Ensure the date is in datetime format
  df_sorted = df.sort_values('Release Date')
  plt.figure(figsize=(10, 6))
  sns.lineplot(x='Release Date', y='Spotify Streams', data=df_sorted)
  plt.title('Spotify Streams Over Time')
  plt.xlabel('Release Date')
  plt.ylabel('Spotify Streams')
  st.pyplot(plt)

def spotify_reach_vs_playlist_count():
  sns.scatterplot(x='Spotify Playlist Count', y='Spotify Playlist Reach', data=df)
  plt.title('Spotify Playlist Reach vs. Playlist Count')
  plt.xlabel('Playlist Count')
  plt.ylabel('Playlist Reach')
  st.pyplot(plt)




if visualization == 'Top 50 Albums by Count':
    Top_50_Albums_by_Count()
elif visualization == 'Top 50 Tracks by Count':
    top_50_tracks_by_count()
elif visualization == 'Top 50 Artists by Count':
    top_50_artists_by_count()
elif visualization == 'Top 20 Ranked Artist':
    top20_ranked_artist()
elif visualization == 'Least 20 Ranked Artist':
    least20_ranked_artist()
elif visualization == 'Top 10 Most Streamed Tracks':
    top_10_most_streamed_tracks()
elif visualization == 'Top 10 Most Streamed Artists':
    top_10_most_streamed_artists()
elif visualization == 'Top 10 Tracks by Playlist Count':
    top_10tracks_by_playlist_count()
elif visualization == 'All Time Rank Popularity':
    all_time_rank_popularity()
elif visualization == 'Spotify Stream Over Time':
    spotify_stream_over_time()
elif visualization == 'Spotify Reach Vs Playlist Count':
    spotify_reach_vs_playlist_count()
 









