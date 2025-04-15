import streamlit as st
import pandas as pd
import json
import os




# Set background image and styles
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                url("https://images.unsplash.com/photo-1568667256549-094345857637?q=80&w=1615&aut"); !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    opacity: 0.9;
}

h1, h2, h3, label, .stTextInput label, .stNumberInput label {
    color: white !important;
    font-weight: bold;
}

/* Styled Sidebar */
[data-testid="stSidebar"] {
    background-color: #C0C0C0 !important; /* Dark gray */
    opacity: 0.95;
    padding-top: 20px;
}


/* Navbar Buttons */
[data-testid="stSidebar"] .stButton>button {
    width: 100%;
    background-color:rgb(155, 174, 195) !important; /* Blue */
    color: black !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-radius: 10px;
    padding: 12px;
    transition: 0.3s;
}

[data-testid="stSidebar"] .stButton>button:hover {
    background-color: #0056b3 !important; /* Darker blue */
}

/* Centered Footer */
footer {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    background: black;
    text-align: center;
    padding: 15px;
    color: white;
    font-size: 20px;
    font-weight: bold;
    border-radius: 10px;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# File to store books
data_file = "library.json"

# Load existing books
if os.path.exists(data_file):
    with open(data_file, "r") as file:
        library = json.load(file)
else:
    library = []

# Convert to DataFrame
def get_library_df():
    return pd.DataFrame(library) if library else pd.DataFrame(columns=["Title", "Author", "Year", "Genre", "Read"])

def save_library():
    with open(data_file, "w") as file:
        json.dump(library, file, indent=4)

def add_book(title, author, year, genre):
    book = {"Title": title, "Author": author, "Year": int(year), "Genre": genre, "Read": False}
    library.append(book)
    save_library()
    st.success(f"📚 Book '{title}' added successfully!", icon="✅")
    st.balloons()

def remove_book(title):
    global library
    updated_library = [book for book in library if book["Title"].lower() != title.lower()]
    if len(updated_library) < len(library):
        library = updated_library
        save_library()
        st.warning(f"🗑️ Book '{title}' removed successfully!", icon="⚠️")
    else:
        st.error("❌ Book not found.", icon="⚠️")

def mark_as_read(title):
    found = False
    for book in library:
        if book["Title"].lower() == title.lower():
            book["Read"] = True
            found = True
            save_library()
            st.balloons()
            st.success(f"✅ Marked '{title}' as read!", icon="📖")
            break
    if not found:
        st.error("❌ Book not found.", icon="⚠️")

st.title("📚 Personal Library Manager")

# Sidebar menu
st.sidebar.header("📌 Menu")
menu_options = ["Add Book", "Remove Book", "View Library", "Search Book", "Statistics"]
selected_option = st.sidebar.radio("📖 Select an option", menu_options)

if selected_option == "Add Book":
    st.subheader("📌 Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("📖 Book Title")
        author = st.text_input("👤 Author")
        year = st.number_input("📅 Publication Year", min_value=1000, max_value=2025, step=1)
        genre = st.text_input("📚 Genre")
        submit_button = st.form_submit_button("✅ Add Book")
        if submit_button:
            add_book(title, author, year, genre)

elif selected_option == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    title = st.text_input("Enter book title to remove")
    if st.button("❌ Remove Book"):
        remove_book(title)

elif selected_option == "View Library":
    st.subheader("📖 Your Book Collection")
    library_df = get_library_df()
    if not library_df.empty:
        st.dataframe(library_df)
    else:
        st.info("📌 No books added yet.", icon="ℹ️")

elif selected_option == "Search Book":
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("Enter book title or author")
    if st.button("🔎 Search"):
        results = [book for book in library if search_query.lower() in book["Title"].lower() or search_query.lower() in book["Author"].lower()]
        if results:
            st.write(pd.DataFrame(results))
        else:
            st.error("❌ No matching books found.", icon="⚠️")

elif selected_option == "Statistics":
    st.subheader("📊 Library Statistics")
    library_df = get_library_df()
    if not library_df.empty:
        st.bar_chart(library_df["Genre"].value_counts())
        st.write("📘 Books Read:", library_df[library_df["Read"] == True].shape[0])
    else:
        st.warning("📌 No books available to analyze.", icon="⚠️")

# Mark book as read section
st.sidebar.subheader("✅ Mark Book as Read")
title = st.sidebar.text_input("📖 Enter book title")
if st.sidebar.button("✔️ Mark as Read"):
    mark_as_read(title)

# Footer
st.markdown("""
    <footer>
       Personal Library Manager | Developed by Rahima |     &copy; 2025  
    </footer>
""", unsafe_allow_html=True)
