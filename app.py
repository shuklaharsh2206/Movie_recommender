import  streamlit as st
import pickle
import pandas as pd
import requests


movies_df = pickle.load(open('movies.pkl','rb'))  # Load the DataFrame and keep it as a DataFrame
similarity = pickle.load(open('similarity.pkl','rb'))



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=7986cb445303f18e9bfc319108c8bb20&language=en-US'.format(movie_id))
    data = response.json()
    
    # Check if 'poster_path' is in the response data
    if 'poster_path' in data and data['poster_path']:
        return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    else:
        # Return a default poster or a placeholder image if 'poster_path' is not available
        return 'path_to_default_poster_or_placeholder_image'  
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]  # Use the DataFrame for indexing
    distances = similarity[movie_index]
    movies_list1 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters=[]
    for i in movies_list1:
        movie_id = movies_df.iloc[i[0]].movie_id  # Correctly fetch the movie_id
        movie_title = movies_df.iloc[i[0]].title  # Fetch the movie title
        recommended_movies.append(movie_title)  # Append the movie title to the list
        # Fetching Posters
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'How Would you like to be contected',
movies_df['title'].values)

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    
    col1 ,col2 ,col3 ,col4 ,col5 =st.columns(5)
    
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])