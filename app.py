

import  streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=198a82101f1ebf47db14729c9802560f&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies =[]
    recommended_movies_posters = []
    for i in movie_list:
        movie_id =movies.iloc[i[0]].movie_id
        #fetch poster
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return  recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies =pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender System')

selected_movie_name =st.selectbox(
'Please select your movie',
movies['title'].values)

if st.button('Recommend'):
    names,posters= recommend(selected_movie_name)

    for i in range(10):
        st.text(names[i])
        st.image(posters[i])


