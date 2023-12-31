from support_functions import \
    read_csv
import streamlit as st

# Configure page config
st.set_page_config(
    page_title="Home",
    page_icon=":musical_note:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# UI components
st.title('Top Songs')

time_range_select = st.selectbox('Time Range', ('Long Term', 'Medium Term', 'Short Term'))

if time_range_select == 'Long Term':
    time_range = 'long_term'
elif time_range_select == 'Medium Term':
    time_range = 'medium_term'
else:
    time_range = 'short_term'

# Collect top song data
song_df = read_csv(f'data/top_song_data_{time_range}.csv')
songs = song_df['song_name']
song_artist = song_df['artist']
song_urls = song_df['image_url']

# Create columns + render images
col1, col2, col3, col4, col5 = st.columns(5, gap="small")

with col1:
    st.image(song_urls[0], caption=f'1. {songs[0]} - {song_artist[0]}')

with col2: 
    st.image(song_urls[1], caption=f'2. {songs[1]} - {song_artist[1]}')

with col3: 
    st.image(song_urls[2], caption=f'3. {songs[2]} - {song_artist[2]}')

with col4: 
    st.image(song_urls[3], caption=f'4. {songs[3]} - {song_artist[3]}')

with col5: 
    st.image(song_urls[4], caption=f'5. {songs[4]} - {song_artist[4]}')
