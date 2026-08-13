import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configuration de la page
st.set_page_config(
    page_title="Data Collection Exam",
    layout="wide"
)

# Connexion à PostgreSQL Neon
database_url = st.secrets["DATABASE_URL"]
engine = create_engine(database_url)

# Chargement des données
books = pd.read_sql("SELECT * FROM books", engine)
gaaraas = pd.read_sql("SELECT * FROM gaaraas", engine)

# Barre latérale
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a dataset",
    ["Books", "Gaaraas"]
)

# Titre principal
st.title("DATA COLLECTION EXAM")
st.write("Web Scraping, Data Visualization and SQL Application")
st.write("Author: Zakaria LOURE")

# PAGE BOOKS
if page == "Books":

    st.header("📚 Books Dashboard")

    # KPI
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Number of books",
            len(books)
        )

    with col2:
        st.metric(
            "Average price",
            f"£{books['prix'].mean():.2f}"
        )

    with col3:
        st.metric(
            "Average rating",
            f"{books['note'].mean():.2f} / 5"
        )

    st.subheader("Books data")
    st.dataframe(books)

# PAGE GAARAAS
else:

    st.header("🚗 Gaaraas Dashboard")

    st.write("Gaaraas dashboard will be added next.")

    st.dataframe(gaaraas)
