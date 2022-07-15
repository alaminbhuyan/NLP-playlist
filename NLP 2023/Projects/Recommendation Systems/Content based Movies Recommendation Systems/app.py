import streamlit as st
import pandas as pd
import pickle
import requests
import numpy as np
import string

st.header("Movie Recommender System")

movie_dict = pickle.load(file=open(file='movie_df3.pkl', mode='rb'))
new_movie_df2 = pd.DataFrame(data=movie_dict)

similarity = pickle.load(file=open(file='similarity4.pkl', mode='rb'))

movie_list = new_movie_df2['title'].values

selected_movie = st.selectbox(label="Type or select a movie from the dropdown", options=movie_list)

# Fetch posters function
def fetchPoster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=667dfa3d96bb189b1badf71dd1ee3c23&language=en-US".format(movie_id)
    data = requests.get(url=url)
    json_data = data.json()
    poster_path = json_data['poster_path']
    full_path = "https://image.tmdb.org/t/p/original" + poster_path
    return full_path

# Movies Recommendation function
def recommender(movie):
    recommended_movies_name = []
    recommended_movies_posters = []
    movie_index = new_movie_df2[new_movie_df2['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x : x[1])
    for i in distances[1:11]:
        # Fetch movie poster
        movie_id = new_movie_df2.loc[i[0], 'movie_id']
        recommended_movies_posters.append(fetchPoster(movie_id = movie_id))
        recommended_movies_name.append(new_movie_df2.loc[i[0], 'title'])

    return (recommended_movies_name, recommended_movies_posters)

if st.button(label="Recommend"):
    recommend_movies_name, recommended_movie_poster = recommender(movie=selected_movie)
    # col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(spec=len(recommend_movies_name))
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    col10, col11, col12 = st.columns(3)

    col1.text(recommend_movies_name[0])
    col1.image(image=recommended_movie_poster[0], use_column_width=True)
    col2.text(recommend_movies_name[1])
    col2.image(image=recommended_movie_poster[1], use_column_width=True)
    col3.text(recommend_movies_name[2])
    col3.image(image=recommended_movie_poster[2], use_column_width=True)
    col4.text(recommend_movies_name[3])
    col4.image(image=recommended_movie_poster[3], use_column_width=True)
    col5.text(recommend_movies_name[4])
    col5.image(image=recommended_movie_poster[4], use_column_width=True)
    col6.text(recommend_movies_name[5])
    col6.image(image=recommended_movie_poster[5], use_column_width=True)
    col7.text(recommend_movies_name[6])
    col7.image(image=recommended_movie_poster[6], use_column_width=True)
    col8.text(recommend_movies_name[7])
    col8.image(image=recommended_movie_poster[7], use_column_width=True)
    col9.text(recommend_movies_name[8])
    col9.image(image=recommended_movie_poster[8], use_column_width=True)
    col10.text(recommend_movies_name[9])
    col10.image(image=recommended_movie_poster[9], use_column_width=True)

    # col1.subheader(recommend_movies_name[0])
    # col1.image(image=recommended_movie_poster[0], use_column_width=True)
    # col2.subheader(recommend_movies_name[1])
    # col2.image(image=recommended_movie_poster[1], use_column_width=True)
    # col3.subheader(recommend_movies_name[2])
    # col3.image(image=recommended_movie_poster[2], use_column_width=True)
    # col4.subheader(recommend_movies_name[3])
    # col4.image(image=recommended_movie_poster[3], use_column_width=True)
    # col5.subheader(recommend_movies_name[4])
    # col5.image(image=recommended_movie_poster[4], use_column_width=True)
    # col6.subheader(recommend_movies_name[5])
    # col6.image(image=recommended_movie_poster[5], use_column_width=True)
    # col7.subheader(recommend_movies_name[6])
    # col7.image(image=recommended_movie_poster[6], use_column_width=True)
    # col8.subheader(recommend_movies_name[7])
    # col8.image(image=recommended_movie_poster[7], use_column_width=True)
    # col9.subheader(recommend_movies_name[8])
    # col9.image(image=recommended_movie_poster[8], use_column_width=True)
    #
    # col10.subheader(recommend_movies_name[9])
    # col10.image(image=recommended_movie_poster[9], use_column_width=True)


