import pickle  # Import the pickle module for loading pickled objects
import streamlit as st  # Import the Streamlit library and alias it as 'st'
import requests  # Import the requests library for making HTTP 
# streamlit run app.py

# Create a sidebar for navigation
st.sidebar.header("Navigation")  # Add a header to the sidebar
selection = st.sidebar.radio("Choose a page", ["About", "Recommendations"])  # Create a radio button for selecting a page

# Define pages as separate functions
def recommendations_page():  # Define a function for the recommendations page
        def fetch_poster(movie_id):  # Define a function to fetch movie posters
            url = "https://api.themoviedb.org/3/movie/{}?api_key=ea4e4a1c97d771d30901b5b0e34c6326&language=en-US".format(movie_id)  # Construct the URL for fetching movie details
            data = requests.get(url)  # Make an HTTP GET request to fetch movie data
            data = data.json()  # Parse the response as JSON
            poster_path = data['poster_path']  # Extract the poster path from the response
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path  # Construct the full URL for the poster image
            return full_path  # Return the full URL of the poster image

        def recommend(movie):  # Define a function to recommend similar movies
            index = movies[movies['title'] == movie].index[0]  # Get the index of the selected movie
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])  # Calculate similarity scores with other movies
            recommended_movie_names = []  # Initialize a list to store recommended movie names
            recommended_movie_posters = []  # Initialize a list to store recommended movie posters
            for i in distances[1:6]:  # Iterate over the top 5 similar movies
                movie_id = movies.iloc[i[0]].movie_id  # Get the movie ID of the recommended movie
                recommended_movie_posters.append(fetch_poster(movie_id))  # Fetch and store the poster of the recommended movie
                recommended_movie_names.append(movies.iloc[i[0]].title)  # Store the title of the recommended movie

            return recommended_movie_names, recommended_movie_posters  # Return the recommended movie names and posters

        st.header('Movie Recommender System')  # Add a header to the recommendations page
        movies = pickle.load(open('movie_list.pkl', 'rb'))  # Load the movie list from a pickled file
        similarity = pickle.load(open('similarity.pkl', 'rb'))  # Load the similarity matrix from a pickled file

        movie_list = movies['title'].values  # Get the list of movie titles
        selected_movie = st.selectbox(  # Create a dropdown to select a movie
            "Type or select a movie from the dropdown",  # Prompt for selecting a movie
            movie_list  # Provide the list of movie titles as options
        )

        if st.button('Show Recommendation'):  # Check if the recommendation button is clicked
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)  # Get recommended movie names and posters
            col1, col2, col3, col4, col5 = st.columns(5)  # Divide the page into 5 columns for displaying recommendations
            with col1:  # Display the first recommended movie in the first column
                st.text(recommended_movie_names[0])  # Display the title of the recommended movie
                st.image(recommended_movie_posters[0])  # Display the poster of the recommended movie
            with col2:  # Display the second recommended movie in the second column
                st.text(recommended_movie_names[1])  # Display the title of the recommended movie
                st.image(recommended_movie_posters[1])  # Display the poster of the recommended movie
            with col3:  # Display the third recommended movie in the third column
                st.text(recommended_movie_names[2])  # Display the title of the recommended movie
                st.image(recommended_movie_posters[2])  # Display the poster of the recommended movie
            with col4:  # Display the fourth recommended movie in the fourth column
                st.text(recommended_movie_names[3])  # Display the title of the recommended movie
                st.image(recommended_movie_posters[3])  # Display the poster of the recommended movie
            with col5:  # Display the fifth recommended movie in the fifth column
                st.text(recommended_movie_names[4])  # Display the title of the recommended movie
                st.image(recommended_movie_posters[4])  # Display the poster of the recommended movie

def about_page():  # Define a function for the about page
    st.header("About This App")  # Add a header to the about page
    st.write("This app explores movie recommendations using a content based recommendation approach.")  # Provide information about the app
    st.markdown('''
                    Here's a general breakdown of the code's steps:  
                    ...
                    ...
                    ...
                    Pickle allows for loading data directly without rerunning preprocessing steps.''')  # Provide a markdown overview of the code's steps

# Call the selected page function
if selection == "Recommendations":  # Check if the selected page is Recommendations
    recommendations_page()  # Call the recommendations page function
elif selection == "About":  # Check if the selected page is About
    about_page()  # Call the about page function
