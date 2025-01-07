import streamlit as st
import pickle, requests
import pandas as pd

# Load movie data and similarity
movies = pickle.load(open('movies_list.pcl', 'rb'))
#similarity = pickle.load(open('similarity.pckl', 'rb'))
movies_genre = pickle.load(open('movies_votes.pcl', 'rb'))
movie_list = movies["title"].values
genre = movies_genre["genre"].unique()  # Assuming there's a 'genre' column
st.set_page_config(layout="wide")

# Function to fetch movie poster
def get_poster(movies_id):
    url = f"https://api.themoviedb.org/3/movie/{movies_id}?api_key=6123614c430cedb24392ce9327d32c62&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(get_poster(movies_id))
    return recommend_movie, recommend_poster

# Function to get movie overview
def get_overview(movies_id):
    url = f"https://api.themoviedb.org/3/movie/{movies_id}?api_key=6123614c430cedb24392ce9327d32c62&language=en-US"
    response = requests.get(url)
    data = response.json()
    return data.get('overview', 'No overview available')

# Function to get top-rated movies by genre
def get_top_movies_by_genre(genre):
    # Filter movies by selected genre
    genre_movies = movies_genre[movies_genre['genre'].str.contains(genre, case=False, na=False)]
    
    # Sort by vote_average in descending order and take the top 10
    top_movies = genre_movies.sort_values(by='vote_average', ascending=False).head(10)
    
    # Return title, id, and vote_average so we can display these later
    return top_movies[['title', 'id', 'vote_average']]

# App Layout
st.markdown(
    "<h1 style='text-align: center;'>🎬📚 Film/Kitap Tavsiye Uygulaması </h1>",
    unsafe_allow_html=True
)

# Columns for layout
col1, col2 = st.columns([5, 5])

# Left column: Movie recommendations
with col1:
    st.subheader("🎬 Movie Recommendation")
    selectvalue = st.selectbox("👇🏽 Select a movie", movie_list)
    if st.button("🍿 Show Movie Recommendations", key="movies"):
        movie_name, movie_poster = recommend(selectvalue)
        movie_cols = st.columns(5)
        for i, col in enumerate(movie_cols):
            with col:
                st.image(movie_poster[i])
                st.text(movie_name[i])

# Right column: Top movies by genre
with col2:
    st.subheader("📋 Top Movies by Genre")
    selected_genre = st.selectbox("Choose a genre", genre, key="select_genre")
    
    if st.button("🎥 Show Top Movies", key="show_top_movies"):
        top_movies = get_top_movies_by_genre(selected_genre)
        
        # Create enough columns based on the number of movies (maximum 5 columns)
        movie_cols = st.columns(min(len(top_movies), 5))  # Ensure max 5 columns
        
        # Iterate through movies and show titles and posters
        for i, (_, row) in enumerate(top_movies.iterrows()):
            if i >= 5:
                break  # Avoid exceeding the column limit
            poster = get_poster(row['id'])
            title = row['title']
            vote_average = row['vote_average']
            
            with movie_cols[i]:
                st.image(poster, caption=title, width=150)  # Set width for the poster
                st.markdown(f"⭐ {vote_average}")  # Show vote average only
                
                # Make the movie title clickable
                if st.button(f"Details for {title}", key=f"btn_{i}"):
                    selected_movie = title
                    overview = row['overview']
                    # Save the selected movie in session_state
                    st.session_state.selected_movie = selected_movie

        # If a movie is selected, show the details immediately
        if 'selected_movie' in st.session_state:
            selected_movie = st.session_state.selected_movie
            poster = get_poster(selected_movie['id'])
            overview = get_overview(selected_movie['id'])
            
            st.subheader(f"📜 {selected_movie['title']} Overview")
            st.image(poster, caption=selected_movie['title'], width=250)
            st.markdown(f"**Overview**: {overview}")
