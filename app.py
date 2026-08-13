import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Titre de l'application
st.title("DATA COLLECTION EXAM")

# Présentation
st.write("Web Scraping, Data Visualization and SQL Application")
st.write("Author: Zakaria LOURE")

# Message de bienvenue
st.success("Welcome to my Data Collection application!")

# Connexion à la base PostgreSQL Neon
database_url = st.secrets["DATABASE_URL"]
engine = create_engine(database_url)

# Lecture des données depuis PostgreSQL
books = pd.read_sql("SELECT * FROM books", engine)
gaaraas = pd.read_sql("SELECT * FROM gaaraas", engine)

# Affichage des données
st.header("Books Data")
st.write(f"Number of books: {len(books)}")
st.dataframe(books)

st.header("Gaaraas Data")
st.write(f"Number of vehicles: {len(gaaraas)}")
st.dataframe(gaaraas)
