import streamlit as st 
import pickle 
import numpy as np 
import pandas as pd 

st.set_page_config(layout="wide")
st.header("📚 Book Recommender System")
st.markdown('''
##### This site uses collaborative filtering to suggest books.
''')


popular = pickle.load(open('popular.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity = pickle.load(open('similarity_scores.pkl','rb')) 


def recommend_books(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        item_data = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title').iloc[0]
        data.append([
             item_data['Book-Title'],
            item_data['Book-Author'],
             item_data['Image-URL-M']
        ])
    return data

def show_book_details(book_title):
    st.markdown("---")
    st.subheader(f"📘 Book Details: {book_title}")
    book_details = books[books['Book-Title'] == book_title].drop_duplicates('Book-Title').iloc[0]

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(book_details['Image-URL-M'])
    with col2:
        st.markdown(f"""
        **Title**: {book_details['Book-Title']}  
        **Author**: {book_details['Book-Author']}  
        **Publisher**: {book_details['Publisher']}  
        **Year of Publication**: {book_details['Year-Of-Publication']}
        """)

    st.markdown("### 📚 You May Also Like")
    recommendations = recommend_books(book_title)
    rec_cols = st.columns(5)
    for i in range(len(recommendations)):
        with rec_cols[i]:
            st.image(recommendations[i][2], use_container_width=True)
            st.caption(recommendations[i][0])
            st.text(recommendations[i][1])


st.sidebar.title("🔎 Search a Book")
search_input = st.sidebar.text_input("Enter book title")
search_btn = st.sidebar.button("Search")


selected_book = None
if search_btn and search_input:
    matching_books = [book for book in pt.index if search_input.lower() in book.lower()]
    if matching_books:
        selected_book = matching_books[0]
    else:
        st.sidebar.warning("Book not found. Please try a different title.")


if 'clicked_book' not in st.session_state:
    st.session_state.clicked_book = None



if selected_book:
    show_book_details(selected_book)
elif st.session_state.clicked_book:
    show_book_details(st.session_state.clicked_book)

st.subheader("🔥 Popular Books")

cols_per_row = 5
num_rows = 10

for row in range(num_rows): 
    cols = st.columns(cols_per_row)
    for col in range(cols_per_row): 
        book_idx = row * cols_per_row + col
        if book_idx < len(popular):
            book_data = popular.iloc[book_idx]
            with cols[col]:
                st.image(book_data['Image-URL-M'], use_container_width=True)
                if st.button(f"View '{book_data['Book-Title']}'", key=f"btn_{book_idx}"):
                    st.session_state.clicked_book = book_data['Book-Title']
                    st.rerun() 
