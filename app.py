import streamlit as st
import pickle
import pandas as pd
import requests

# Load movie data and similarity matrix
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Define function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7986cb445303f18e9bfc319108c8bb20&language=en-US')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    else:
        return 'path_to_default_poster_or_placeholder_image'

# Define recommendation function
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list1 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list1:
        movie_id = movies_df.iloc[i[0]].movie_id
        movie_title = movies_df.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Styling for the front page
st.markdown(
    """
    <style>
    .stFrontPage {
        text-align: center;
        margin-top: 50px;
    }
    .stTitle {
        font-size: 50px;
        font-weight: bold;
        color: #FF6347;
    }
    .stSubtitle {
        font-size: 20px;
        color: #4CAF50;
        margin-bottom: 30px;
    }
    .stStartButton {
        margin-top: 50px;
    }
    .stImage {
        max-width: 60%;
        height: auto;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Implement front page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'front_page'

if st.session_state.page == 'front_page':
    st.markdown('<div class="stFrontPage">', unsafe_allow_html=True)
    st.markdown('<div class="stTitle">Welcome to the Movie Recommender System</div>', unsafe_allow_html=True)
    st.markdown('<div class="stSubtitle">Discover your next favorite movie based on what you love!</div>', unsafe_allow_html=True)

    # Adding a movie-themed image
    st.image('https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg', caption="Your Ultimate Movie Guide", use_column_width=True)

    # Start button to navigate to the main app
    if st.button('Get Started', key='start_button'):
        st.session_state.page = 'main'

elif st.session_state.page == 'main':
    # Main Movie Recommender Page
    st.markdown(
        """
        <style>
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            border: 2px solid #4CAF50;
            color: white;
            padding: 14px 28px;
            font-size: 16px;
            cursor: pointer;
            background-color: #4CAF50;
        }
        .stButton>button:hover {
            background-color: white;
            color: #4CAF50;
        }
        .stTitle {
            font-size: 40px;
            font-weight: bold;
            color: #FF6347;
            text-align: center;
            margin-bottom: 50px;
        }
        .stSelectbox {
            width: 50%;
            margin: auto;
            border: 2px solid #FF6347;
            border-radius: 20px;
        }
        .stImage {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        }
        .stText {
            font-size: 18px;
            color: #4CAF50;
            text-align: center;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="stTitle">Movie Recommender System</div>', unsafe_allow_html=True)

    # Movie selection and recommendation display
    selected_movie_name = st.selectbox(
        'Choose a movie you like and get recommendations:',
        movies_df['title'].values,
        format_func=lambda x: '🎬 ' + x
    )

    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)
        cols = st.columns(5)

        # Display recommended movies and their posters
        for i in range(len(names)):
            with cols[i]:
                st.markdown(f'<div class="stText">{names[i]}</div>', unsafe_allow_html=True)
                st.image(posters[i], use_column_width=True, output_format='PNG')
