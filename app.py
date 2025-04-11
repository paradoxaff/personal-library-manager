
import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="Personal Library",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Personal Library App")

if "all_books" not in st.session_state:
    st.session_state.all_books = []

menu = st.sidebar.radio("Menu", [
    "Add a Book",
    "Remove a Book",
    "Search for a Book",
    "Display All Books",
    "Display Statistics"
])

if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    with st.form("add_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.text_input("Publication Year")
        genre = st.text_input("Genre")
        read = st.selectbox("Have you read this book?", ["yes", "no"])
        submitted = st.form_submit_button("Add Book")

        if submitted:
            book = {
                "title": title,
                "author": author,
                "publication-year": year,
                "genre": genre,
                "read": read
            }
            st.session_state.all_books.append(book)
            st.success("Book added successfully!")

elif menu == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    if not st.session_state.all_books:
        st.info("No books to remove.")
    else:
        titles = [book["title"] for book in st.session_state.all_books]
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            st.session_state.all_books = [book for book in st.session_state.all_books if book["title"] != book_to_remove]
            st.success(f"'{book_to_remove}' has been removed.")

elif menu == "Search for a Book":
    st.subheader("🔍 Search for a Book")
    search_title = st.text_input("Enter book title to search")
    if st.button("Search"):
        found = False
        for book in st.session_state.all_books:
            if book["title"].lower() == search_title.lower():
                st.success("Book Found:")
                st.write(book)
                found = True
                break
        if not found:
            st.error("Book not found in your library.")

elif menu == "Display All Books":
    st.subheader("📖 Your Book List")
    if not st.session_state.all_books:
        st.info("Your library is empty.")
    else:
        df = pd.DataFrame(st.session_state.all_books)
        st.dataframe(df, use_container_width=True)

elif menu == "Display Statistics":
    st.subheader("📊 Library Statistics")
    if not st.session_state.all_books:
        st.info("No statistics available. Your library is empty.")
    else:
        total = len(st.session_state.all_books)
        read = sum(1 for b in st.session_state.all_books if b["read"].lower() == "yes")
        unread = total - read
        percentage = (read / total) * 100

        st.metric("Total Books", total)
        st.metric("Books Read", read)
        st.metric("Books Unread", unread)
        st.metric("% Read", f"{percentage:.1f}%")
