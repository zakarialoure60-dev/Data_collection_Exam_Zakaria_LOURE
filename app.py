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


# ============================================
# PAGE BOOKS
# ============================================

if page == "Books":

    st.header("📚 Books Dashboard")

    # -------------------------
    # FILTRES
    # -------------------------

    st.subheader("Filters")

    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        max_price = st.slider(
            "Maximum price (£)",
            min_value=float(books["prix"].min()),
            max_value=float(books["prix"].max()),
            value=float(books["prix"].max())
        )

    with col_filter2:
        min_rating = st.selectbox(
            "Minimum rating",
            [1, 2, 3, 4, 5],
            index=0
        )

    # Application des filtres
    books_filtered = books[
        (books["prix"] <= max_price) &
        (books["note"] >= min_rating)
    ]

    # -------------------------
    # KPI
    # -------------------------

    st.subheader("Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Number of books",
            len(books_filtered)
        )

    with col2:
        average_price = books_filtered["prix"].mean()

        st.metric(
            "Average price",
            f"£{average_price:.2f}"
            if not books_filtered.empty
            else "N/A"
        )

    with col3:
        average_rating = books_filtered["note"].mean()

        st.metric(
            "Average rating",
            f"{average_rating:.2f} / 5"
            if not books_filtered.empty
            else "N/A"
        )

    # -------------------------
    # GRAPHIQUES
    # -------------------------

    st.subheader("Data Visualization")

    chart_col1, chart_col2 = st.columns(2)

    # Répartition des livres par note
    with chart_col1:

        rating_counts = (
            books_filtered["note"]
            .value_counts()
            .sort_index()
        )

        st.write("Books by rating")

        st.bar_chart(rating_counts)

    # Prix moyen par note
    with chart_col2:

        average_price_by_rating = (
            books_filtered
            .groupby("note")["prix"]
            .mean()
        )

        st.write("Average price by rating")

        st.bar_chart(average_price_by_rating)

    # -------------------------
    # TABLEAU
    # -------------------------

    st.subheader("Books data")

    st.dataframe(
        books_filtered,
        use_container_width=True
    )


# ============================================
# PAGE GAARAAS
# ============================================

else:

    st.header("🚗 Gaaraas Dashboard")

    st.write("Gaaraas dashboard will be added next.")

    st.dataframe(
        gaaraas,
        use_container_width=True
    )
