import streamlit as st
import pickle
import pandas as pd
import requests

#Function to fetch poster from TMDB API
def fetch_poster_by_id(movie_id):
    api_key = "10f23f95b3b22ec7284505e2069716fc"  #TMDB v3 API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)
    data = response.json()

    if "poster_path" in data and data["poster_path"]:
        full_url = "https://image.tmdb.org/t/p/w500" + data["poster_path"]
        return full_url
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

#Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Get TMDB movie ID
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster_by_id(movie_id))

    return recommended_movies, recommended_posters

#Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

#Streamlit UI
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie to get similar recommendations:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
