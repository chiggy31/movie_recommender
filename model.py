import streamlit as st 
import pickle
import pandas as pd
import requests
from PIL import Image

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b30555f57c545f1ce93bb3afaa948d11'.format(movie_id)
)
    data = response.json()
    return  "https://image.tmdb.org/t/p/w500/"+ data['poster_path']


def recommend(movie):
    movie_ind = movies_list[movies_list['title'] == movie].index[0]
    dist = similarity[movie_ind]
    movie_list = sorted(list(enumerate(dist)) , reverse=True , key= lambda x : x[1])[1:6]
    rec_movies = []
    rec_poster = []
    for i in movie_list :
        movie_id = movies_list.iloc[i[0]].movie_id
        # fetch poster
        rec_movies.append(movies_list.iloc[i[0]].title)
        rec_poster.append(fetch_poster(movie_id)) 
    return rec_movies,rec_poster


# Display an image
image = Image.open('Designer.png')
image = image.resize((800, 400))
st.image(image, use_column_width=True)

st.title('Movie recommendor systems')

#load data 
movies_dict = pickle.load(open('movies.pkl','rb'))
movies_list = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# Movie selection
option = st.selectbox(
    "Which type of movies would you like to watch ?",
    movies_list['title'].values)

st.write("You selected:", option)

#  button layout
c1 , c2 ,c3  = st.columns([1,1,1])
# recommend button
with c1 :
    recommend_button = st.button("Recommend" , type="primary")
# reset button
with c3 : 
    reset_button = st.button("Reset", type="secondary")

    
if recommend_button:
    names,posters = recommend(option)
    # for i in recomendations:
    #     st.write(i)
    col1, col2, col3 ,col4,col5= st.columns(5)
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

else:
    st.write("press recommend to see results")

# Add a footer
st.empty()
st.markdown("""
    <style>
    .footer {
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: black;
        color: orange;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Created by Chirag Goyal | Contact: <a href="mailto:chiragunion212@gmail.com">chiragunion212@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)


