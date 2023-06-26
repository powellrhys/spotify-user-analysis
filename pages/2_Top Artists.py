import streamlit as st
from support_functions import read_csv

# Configure page config
st.set_page_config(
    page_title="Home",
    page_icon=":musical_note:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title('Top Artists')

time_range_select = st.selectbox('Time Range', ('Long Term', 'Medium Term', 'Short Term'))

if time_range_select == 'Long Term':
    time_range = 'long_term'
elif time_range_select == 'Medium Term':
    time_range = 'medium_term'
else:
    time_range = 'short_term'

artist_df = read_csv(f'data/top_artist_data_{time_range}.csv')

artist = artist_df['artist']
artist_url = artist_df['image_url']

col1, col2, col3, col4, col5 = st.columns(5, gap="small")

with col1:
    st.image(artist_url[0], caption=f'1. {artist[0]}')

with col2: 
    st.image(artist_url[1], caption=f'2. {artist[1]}')

with col3: 
    st.image(artist_url[2], caption=f'3. {artist[2]}')

with col4: 
    st.image(artist_url[3], caption=f'4. {artist[3]}')

with col5: 
    st.image(artist_url[4], caption=f'5. {artist[4]}')
