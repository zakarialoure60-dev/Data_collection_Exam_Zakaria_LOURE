import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# ============================================
# CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Data Collection Exam",
    layout="wide"
)

# ============================================
# CONNEXION POSTGRESQL NEON
# ============================================

database_url = st.secrets["DATABASE_URL"]
engine = create_engine(database_url)

# Chargement des données depuis PostgreSQL
books = pd.read_sql("SELECT * FROM books", engine)
gaaraas = pd.read_sql("SELECT * FROM gaaraas", engine)

# ============================================
# NAVIGATION
# ============================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a dataset",
    ["Books", "Gaaraas"]
)

# ============================================
# TITRE PRINCIPAL
# ============================================

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

    with chart_col1:

        rating_counts = (
            books_filtered["note"]
            .value_counts()
            .sort_index()
        )

        st.write("Books by rating")

        st.bar_chart(rating_counts)

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

    # -------------------------
    # FILTRES
    # -------------------------

    st.subheader("Filters")

    col_filter1, col_filter2, col_filter3 = st.columns(3)

    # Liste des marques
    brands = sorted(
        gaaraas["marque"]
        .dropna()
        .unique()
        .tolist()
    )

    with col_filter1:

        selected_brand = st.selectbox(
            "Brand",
            ["All"] + brands
        )

    with col_filter2:

        max_vehicle_price = st.slider(
            "Maximum price",
            min_value=float(gaaraas["prix"].min()),
            max_value=float(gaaraas["prix"].max()),
            value=float(gaaraas["prix"].max())
        )

    with col_filter3:

        min_year = st.slider(
            "Minimum year",
            min_value=int(gaaraas["annee"].min()),
            max_value=int(gaaraas["annee"].max()),
            value=int(gaaraas["annee"].min())
        )

    # -------------------------
    # APPLICATION DES FILTRES
    # -------------------------

    gaaraas_filtered = gaaraas[
        (gaaraas["prix"] <= max_vehicle_price) &
        (gaaraas["annee"] >= min_year)
    ]

    if selected_brand != "All":

        gaaraas_filtered = gaaraas_filtered[
            gaaraas_filtered["marque"] == selected_brand
        ]

    # -------------------------
    # KPI
    # -------------------------

    st.subheader("Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Number of vehicles",
            len(gaaraas_filtered)
        )

    with col2:

        average_vehicle_price = (
            gaaraas_filtered["prix"].mean()
        )

        st.metric(
            "Average price",
            f"{average_vehicle_price:,.0f}"
            if not gaaraas_filtered.empty
            else "N/A"
        )

    with col3:

        average_mileage = (
            gaaraas_filtered["kilometrage"].mean()
        )

        st.metric(
            "Average mileage",
            f"{average_mileage:,.0f} km"
            if not gaaraas_filtered.empty
            else "N/A"
        )

    # -------------------------
    # GRAPHIQUES
    # -------------------------

    st.subheader("Data Visualization")

    chart_col1, chart_col2 = st.columns(2)

    # Nombre de véhicules par marque
    with chart_col1:

        vehicles_by_brand = (
            gaaraas_filtered["marque"]
            .value_counts()
            .head(10)
        )

        st.write("Top 10 brands by number of vehicles")

        st.bar_chart(vehicles_by_brand)

    # Prix moyen par marque
    with chart_col2:

        price_by_brand = (
            gaaraas_filtered
            .groupby("marque")["prix"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )

        st.write("Top 10 brands by average price")

        st.bar_chart(price_by_brand)

    # -------------------------
    # TABLEAU
    # -------------------------

    st.subheader("Gaaraas data")

    st.dataframe(
        gaaraas_filtered,
        use_container_width=True
    )
