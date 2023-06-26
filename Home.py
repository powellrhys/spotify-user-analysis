import streamlit as st
from support_functions import read_csv

# Configure page config
st.set_page_config(
    page_title="Home",
    page_icon=":musical_note:",
    layout="wide"
)

time_range_select = st.selectbox('Time Range', ('Long Term', 'Medium Term', 'Short Term'))

if time_range_select == 'Long Term':
    time_range = 'long_term'
elif time_range_select == 'Medium Term':
    time_range = 'medium_term'
else:
    time_range = 'short_term'

df = read_csv(f'data/song_data_{time_range}.csv')

songs = df['song_name']
artist = df['artist']
urls = df['image_url']

col1, col2, col3, col4, col5 = st.columns(5, gap="small")

with col1:
    st.image(urls[0], caption=f'1. {songs[0]} - {artist[0]}')

with col2: 
    st.image(urls[1], caption=f'2. {songs[1]} - {artist[1]}')

with col3: 
    st.image(urls[2], caption=f'3. {songs[2]} - {artist[2]}')

with col4: 
    st.image(urls[3], caption=f'4. {songs[3]} - {artist[3]}')

with col5: 
    st.image(urls[4], caption=f'5. {songs[4]} - {artist[4]}')
