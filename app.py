import pickle
import streamlit as st
import requests
# streamlit run app.py

# Create a sidebar for navigation
st.sidebar.header("Navigation")
selection = st.sidebar.radio("Choose a page", [ "About","Recommendations"])

# Define pages as separate functions
def recommendations_page():
        def fetch_poster(movie_id):
            url = "https://api.themoviedb.org/3/movie/{}?api_key=ea4e4a1c97d771d30901b5b0e34c6326&language=en-US".format(movie_id)
            data = requests.get(url)
            data = data.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path

        def recommend(movie):
            index = movies[movies['title'] == movie].index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            recommended_movie_names = []
            recommended_movie_posters = []
            for i in distances[1:6]:
                # fetch the movie poster form Api
                movie_id = movies.iloc[i[0]].movie_id
                recommended_movie_posters.append(fetch_poster(movie_id))
                recommended_movie_names.append(movies.iloc[i[0]].title)

            return recommended_movie_names,recommended_movie_posters

        st.header('Movie Recommender System')
        movies = pickle.load(open('movie_list.pkl','rb'))
        similarity = pickle.load(open('similarity.pkl','rb'))

        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Type or select a movie from the dropdown",
            movie_list
        )

        if st.button('Show Recommendation'):
            recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0])
            with col2:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])

            with col3:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])
            with col4:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])
            with col5:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])

def about_page():
    st.header("About This App")
    st.write("This app explores movie recommendations using a content based recommendation approach.")
    # ... (add more details about the app and its creators)
    st.markdown('''
                    Here's a general breakdown of the code's steps:

                    1. Importing Libraries:

                    . Imports NumPy for numerical operations and pandas for data manipulation.
                
                    2. Loading Datasets:

                    . Reads two CSV files, tmdb_5000_movies.csv and tmdb_5000_credits.csv, into pandas DataFrames.
                    . Merges these DataFrames on the 'title' column to create a combined dataset.
                
                    3. Data Preprocessing:
                
                    · Cleans and prepares the data for analysis:
                    . Converts stringified lists to actual lists for genres and keywords.
                    . Handles missing values (drops rows with NaN).
                    . Extracts the first 3 cast members and the director for each movie.
                    · Splits movie overviews into words.
                    · Removes spaces from names to avoid duplicates.
                    · Creates a new column 'tags' by combining overview, genres, keywords, cast, and crew.
                    . Converts all words in 'tags' to lowercase for consistency.

                    4. Text Vectorization:
                
                    · Transforms text data into numerical representations for analysis:
                    · Uses CountVectorizer to create a matrix of word counts (considering 5000 most common words,
                    excluding stop words).
                    . Employs PorterStemmer for stemming (reducing words to their root forms).
                    Recreates the numerical matrix after stemming for more accurate comparisons.
                
                    5. Calculating Similarity:
                
                    · Computes cosine similarity between movies based on their vector representations:
                    · Cosine similarity measures closeness in terms of word usage.
                    . Higher similarity scores indicate more similar movies.
                
                    6. Building a Recommendation Function:
                
                    · Defines a function recommend(movie) to recommend similar movies:
                    . Finds the index of the input movie in the dataset.
                    . Sorts other movies based on their similarity scores to the input movie.
                    . Prints the titles of the top 5 most similar movies.
                
                    7. Saving Data:
                
                    · Pickles the processed dataset and similarity matrix for later use:
                    . Pickle allows for loading data directly without rerunning preprocessing steps.''')

# Call the selected page function
if selection == "Recommendations":
    recommendations_page()
elif selection == "About":
    about_page()
