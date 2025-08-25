
import pickle # importing pickle files
import requests #getting http responses
import streamlit as st #creating simplke web application
import time # used regulate function flow and wait timing
from dotenv import load_dotenv
import os
load_dotenv()
API_BEARER = os.getenv("API_BEARER")

st.html("<style>[alt='Logo'] { height: 60px !important; }</style>")
st.logo("C:/Users/Admin/Desktop/Movie recommendation/myapp/oflix_logo.png")
page_bg_img = """ 
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://wallpapers.com/images/hd/netflix-background-gs7hjuwvv2g0e9fj.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;

}
</style>
"""# CSS code for background image
st.markdown(page_bg_img, unsafe_allow_html=True) # to allow streamlit to use css code



st.header("🍿 MOVIE RECOMMENDATION SYSTEM 📽️") # HEADING

# Load data
movies = pickle.load(open('artifacts/movies.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox('Type or select a movie', movie_list)

# =====================
# Fetch Poster
# =====================
@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?&language=en-US"

    headers = {
         "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
         "accept": "application/json",
         "Authorization": f"Bearer {API_BEARER}"
        }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"

# =====================
# Recommend Movies
# =====================
def recommend(movie_title, n=5):
    if movie_title not in movies['title'].values:
        return [], [], []

    index = movies[movies['title'] == movie_title].index[0]
    distances = list(enumerate(similarity[index]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:n+1]

    names, posters, links = [], [], []
    for movie in sorted_movies:
        movie_id = movies.iloc[movie[0]].id
        title = movies.iloc[movie[0]].title 
        posters.append(fetch_poster(movie_id))
        names.append(movies.iloc[movie[0]].title)
        links.append(f"https://www.justwatch.com/in/movie/{title.replace(" ","-").replace(":","-")}")
        time.sleep(1)

    return names, posters, links

# =====================
# Show Recommendations
# =====================


if st.button('Show recommendations'):
    if selected_movie:
        st.title("Selected Movie:")
        movie_id = movies[movies['title'] == selected_movie].iloc[0].id
        poster = fetch_poster(movie_id)
        movie_link = f"https://www.justwatch.com/in/movie/{selected_movie.replace(' ', '-').replace(':','-')}"

        st.markdown(
            f'<a href="{movie_link}" target="_blank">'
            f'<img src="{poster}" width="200"></a>',
            unsafe_allow_html=True
        )

    names, posters, links = recommend(selected_movie)
    st.title("RECOMMENDED")
    cols = st.columns(len(names))
    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f'<a href="{links[i]}" target="_blank">'
                f'<img src="{posters[i]}" width="150"></a>',
                unsafe_allow_html=True
            )
            st.write(names[i])
footer = """
<div style="
    position: fixed;
    bottom: 10px;
    left: 10px;
    color: aliceblue;
    font-size: large;
">
    Created by <a href="https://www.linkedin.com/in/rohitkpsingh" target="_blank" style="color: aliceblue; text-decoration: none;">
        Rohit Singh
    </a>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)