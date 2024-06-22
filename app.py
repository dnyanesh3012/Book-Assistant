import requests
import streamlit as st

# Define API base URL
API_URL = "http://127.0.0.1:8000"

def get_top_100_books(genre):
    response = requests.get(f"{API_URL}/top100/{genre}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching top 100 books: {response.status_code}")

def get_top_10_books(genre):
    response = requests.get(f"{API_URL}/top10/{genre}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching top 10 books: {response.status_code}")

def recommend_book(genre, book_title):
    response = requests.get(f"{API_URL}/recommend/{genre}/{book_title}")
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        st.error("Book not found.")
    else:
        st.error(f"Error fetching recommended book: {response.status_code}")

def main():
    st.title("Book Recommendation Agent")

    genre = st.text_input("Enter a genre:", "Fiction")
    if st.button("Get Top 100 Books"):
        top_100_books = get_top_100_books(genre)
        if top_100_books:
            st.write("Top 100 Books:")
            st.write(top_100_books)

    if st.button("Get Top 10 Books"):
        top_10_books = get_top_10_books(genre)
        if top_10_books:
            st.write("Top 10 Books:")
            st.write(top_10_books)

    book_title = st.text_input("Enter a book title from top 10:", "")
    if st.button("Recommend Book"):
        recommended_book = recommend_book(genre, book_title)
        if recommended_book:
            st.write("Recommended Book:")
            st.write(recommended_book)

if __name__ == "__main__":
    main()
