# Importing necessary libraries
import streamlit as st
import pickle 
import pandas as pd
import requests

# Create a fetch function that will fetch posters from the API
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f874fda0db3d481120ee413cd7ddc8e0&&language=en-US'. format(movie_id))
    data = response.json()
    # The complete poster path
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
# End of function

# Create a recommender function
def recommend(movie):
    # Fetching the index of the selected movie
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetching the poster from the API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters
# End of function

# Loading the movie data from the pickled file
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# Creating a dataframe from the loaded dictionary
movies = pd.DataFrame(movies_dict)

# Loading the similarity matrix from the pickled file
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title
st.title('Movie Recommender System')

# Dropdown/selectbox for choosing a movie
selected_movie_name = st.selectbox(
    'Hi! Please select a Movie by either the dropdown option or by typing it!!',
     movies['title'].values
)

# Adding a recommending button
if st.button('Recommend'):
    # Calling the recommend function and getting recommended movie names and posters
    names, posters = recommend(selected_movie_name)

    # Displaying the recommended movies and posters in columns
    col1, col2, col3, col4, col5 = st.columns(5)
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