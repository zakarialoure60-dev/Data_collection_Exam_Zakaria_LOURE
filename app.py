import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import shutil
import time


# ============================================
# CONFIGURATION DE LA PAGE
# ============================================

st.set_page_config(
    page_title="Data Collection Exam",
    page_icon="📊",
    layout="wide"
)


# ============================================
# CONNEXION POSTGRESQL NEON
# ============================================

database_url = st.secrets["DATABASE_URL"]

engine = create_engine(database_url)


# ============================================
# CHARGEMENT DES DONNEES SQL
# ============================================

@st.cache_data(ttl=300)
def load_data():

    books = pd.read_sql(
        "SELECT * FROM books",
        engine
    )

    gaaraas = pd.read_sql(
        "SELECT * FROM gaaraas",
        engine
    )

    return books, gaaraas


books, gaaraas = load_data()


# ============================================
# NAVIGATION
# ============================================

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Choose a section",
    [
        "📚 Books Dashboard",
        "🚗 Gaaraas Dashboard",
        "🕷️ Live Scraping"
    ]
)


st.sidebar.markdown("---")

st.sidebar.write(
    "Data Collection Exam"
)

st.sidebar.write(
    "Zakaria LOURE"
)


# ============================================
# TITRE PRINCIPAL
# ============================================

st.title("DATA COLLECTION EXAM")

st.write(
    "Web Scraping, Data Visualization and SQL Application"
)

st.write(
    "Author: Zakaria LOURE"
)


# ==========================================================
# PAGE 1 : BOOKS
# ==========================================================

if page == "📚 Books Dashboard":

    st.header("📚 Books Dashboard")

    st.caption(
        "Cleaned Selenium data stored in PostgreSQL Neon"
    )


    # ----------------------------------------
    # FILTRES
    # ----------------------------------------

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
        (books["prix"] <= max_price)
        &
        (books["note"] >= min_rating)
    ]


    # ----------------------------------------
    # KPI
    # ----------------------------------------

    st.subheader(
        "Key Performance Indicators"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Number of books",
            len(books_filtered)
        )


    with col2:

        average_price = (
            books_filtered["prix"].mean()
        )

        if books_filtered.empty:

            st.metric(
                "Average price",
                "N/A"
            )

        else:

            st.metric(
                "Average price",
                f"£{average_price:.2f}"
            )


    with col3:

        average_rating = (
            books_filtered["note"].mean()
        )

        if books_filtered.empty:

            st.metric(
                "Average rating",
                "N/A"
            )

        else:

            st.metric(
                "Average rating",
                f"{average_rating:.2f} / 5"
            )


    # ----------------------------------------
    # GRAPHIQUES
    # ----------------------------------------

    st.subheader(
        "Data Visualization"
    )


    chart_col1, chart_col2 = st.columns(2)


    with chart_col1:

        rating_counts = (
            books_filtered["note"]
            .value_counts()
            .sort_index()
        )

        st.write(
            "Books by rating"
        )

        st.bar_chart(
            rating_counts
        )


    with chart_col2:

        average_price_by_rating = (
            books_filtered
            .groupby("note")["prix"]
            .mean()
        )

        st.write(
            "Average price by rating"
        )

        st.bar_chart(
            average_price_by_rating
        )


    # ----------------------------------------
    # TABLE
    # ----------------------------------------

    st.subheader(
        "Books data"
    )

    st.dataframe(
        books_filtered,
        use_container_width=True
    )


# ==========================================================
# PAGE 2 : GAARAAS
# ==========================================================

elif page == "🚗 Gaaraas Dashboard":

    st.header(
        "🚗 Gaaraas Dashboard"
    )

    st.caption(
        "Cleaned Selenium data stored in PostgreSQL Neon"
    )


    # ----------------------------------------
    # FILTRES
    # ----------------------------------------

    st.subheader(
        "Filters"
    )


    col_filter1, col_filter2, col_filter3 = (
        st.columns(3)
    )


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
            min_value=float(
                gaaraas["prix"].min()
            ),
            max_value=float(
                gaaraas["prix"].max()
            ),
            value=float(
                gaaraas["prix"].max()
            )
        )


    with col_filter3:

        min_year = st.slider(
            "Minimum year",
            min_value=int(
                gaaraas["annee"].min()
            ),
            max_value=int(
                gaaraas["annee"].max()
            ),
            value=int(
                gaaraas["annee"].min()
            )
        )


    # ----------------------------------------
    # APPLICATION DES FILTRES
    # ----------------------------------------

    gaaraas_filtered = gaaraas[
        (gaaraas["prix"] <= max_vehicle_price)
        &
        (gaaraas["annee"] >= min_year)
    ]


    if selected_brand != "All":

        gaaraas_filtered = (
            gaaraas_filtered[
                gaaraas_filtered["marque"]
                ==
                selected_brand
            ]
        )


    # ----------------------------------------
    # KPI
    # ----------------------------------------

    st.subheader(
        "Key Performance Indicators"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Number of vehicles",
            len(gaaraas_filtered)
        )


    with col2:

        average_vehicle_price = (
            gaaraas_filtered["prix"]
            .mean()
        )

        if gaaraas_filtered.empty:

            st.metric(
                "Average price",
                "N/A"
            )

        else:

            st.metric(
                "Average price",
                f"{average_vehicle_price:,.0f} CFA"
            )


    with col3:

        average_mileage = (
            gaaraas_filtered[
                "kilometrage"
            ].mean()
        )

        if gaaraas_filtered.empty:

            st.metric(
                "Average mileage",
                "N/A"
            )

        else:

            st.metric(
                "Average mileage",
                f"{average_mileage:,.0f} km"
            )


    # ----------------------------------------
    # GRAPHIQUES
    # ----------------------------------------

    st.subheader(
        "Data Visualization"
    )


    chart_col1, chart_col2 = st.columns(2)


    with chart_col1:

        vehicles_by_brand = (
            gaaraas_filtered["marque"]
            .value_counts()
            .head(10)
        )

        st.write(
            "Top 10 brands by number of vehicles"
        )

        st.bar_chart(
            vehicles_by_brand
        )


    with chart_col2:

        price_by_brand = (
            gaaraas_filtered
            .groupby("marque")["prix"]
            .mean()
            .sort_values(
                ascending=False
            )
            .head(10)
        )

        st.write(
            "Top 10 brands by average price"
        )

        st.bar_chart(
            price_by_brand
        )


    # ----------------------------------------
    # TABLE
    # ----------------------------------------

    st.subheader(
        "Gaaraas data"
    )

    st.dataframe(
        gaaraas_filtered,
        use_container_width=True
    )


# ==========================================================
# PAGE 3 : LIVE SCRAPING
# ==========================================================

else:

    st.header(
        "🕷️ Live Web Scraping"
    )

    st.write(
        "Launch a Selenium scraping directly "
        "from the Streamlit application."
    )

    st.info(
        "For the live demonstration, the application "
        "scrapes Books to Scrape over several pages."
    )


    # ----------------------------------------
    # PARAMETRES
    # ----------------------------------------

    st.subheader(
        "Scraping parameters"
    )


    number_pages = st.number_input(
        "Number of pages to scrape",
        min_value=1,
        max_value=5,
        value=1,
        step=1
    )


    st.caption(
        "The live demo is limited to 5 pages "
        "to keep execution time reasonable."
    )


    # ----------------------------------------
    # BOUTON DE SCRAPING
    # ----------------------------------------

    if st.button(
        "🚀 Start scraping",
        type="primary"
    ):

        driver = None

        try:

            # --------------------------------
            # LOCALISATION CHROMIUM
            # --------------------------------

            chromium_path = (
                shutil.which("chromium")
                or
                shutil.which("chromium-browser")
            )

            chromedriver_path = (
                shutil.which("chromedriver")
            )


            if chromium_path is None:

                st.error(
                    "Chromium was not found."
                )

                st.stop()


            if chromedriver_path is None:

                st.error(
                    "ChromeDriver was not found."
                )

                st.stop()


            # --------------------------------
            # CONFIGURATION SELENIUM
            # --------------------------------

            options = webdriver.ChromeOptions()

            options.binary_location = (
                chromium_path
            )

            options.add_argument(
                "--headless"
            )

            options.add_argument(
                "--no-sandbox"
            )

            options.add_argument(
                "--disable-dev-shm-usage"
            )

            options.add_argument(
                "--disable-gpu"
            )

            options.add_argument(
                "--window-size=1920,1080"
            )


            service = Service(
                chromedriver_path
            )


            driver = webdriver.Chrome(
                service=service,
                options=options
            )


            # --------------------------------
            # STOCKAGE
            # --------------------------------

            collected_data = []


            progress_bar = (
                st.progress(0)
            )


            status_text = st.empty()


            # --------------------------------
            # BOUCLE MULTI-PAGES
            # --------------------------------

            for page_number in range(
                1,
                int(number_pages) + 1
            ):

                status_text.write(
                    f"Scraping page "
                    f"{page_number}..."
                )


                url = (
                    "https://books.toscrape.com/"
                    "catalogue/"
                    f"page-{page_number}.html"
                )


                driver.get(url)

                time.sleep(1)


                # --------------------------------
                # CONTENEURS PRODUITS
                # --------------------------------

                containers = (
                    driver.find_elements(
                        By.CSS_SELECTOR,
                        "article.product_pod"
                    )
                )


                products_on_page = len(
                    containers
                )


                # --------------------------------
                # EXTRACTION
                # --------------------------------

                for container in containers:

                    try:

                        title = (
                            container
                            .find_element(
                                By.CSS_SELECTOR,
                                "h3 a"
                            )
                            .get_attribute(
                                "title"
                            )
                        )

                    except:

                        title = None


                    try:

                        price = (
                            container
                            .find_element(
                                By.CSS_SELECTOR,
                                "p.price_color"
                            )
                            .text
                        )

                    except:

                        price = None


                    try:

                        availability = (
                            container
                            .find_element(
                                By.CSS_SELECTOR,
                                "p.instock.availability"
                            )
                            .text
                            .strip()
                        )

                    except:

                        availability = None


                    try:

                        rating_class = (
                            container
                            .find_element(
                                By.CSS_SELECTOR,
                                "p.star-rating"
                            )
                            .get_attribute(
                                "class"
                            )
                        )

                        rating = (
                            rating_class
                            .replace(
                                "star-rating",
                                ""
                            )
                            .strip()
                        )

                    except:

                        rating = None


                    collected_data.append(
                        {
                            "Page":
                                page_number,

                            "Titre":
                                title,

                            "Prix":
                                price,

                            "Disponibilite":
                                availability,

                            "Nombre_produits":
                                products_on_page,

                            "Note":
                                rating
                        }
                    )


                progress_bar.progress(
                    page_number
                    /
                    int(number_pages)
                )


            # --------------------------------
            # CREATION DATAFRAME
            # --------------------------------

            live_df = pd.DataFrame(
                collected_data
            )


            # --------------------------------
            # RESULTATS
            # --------------------------------

            status_text.success(
                "Scraping completed!"
            )


            st.success(
                f"{len(live_df)} products "
                f"scraped from "
                f"{number_pages} page(s)."
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Pages scraped",
                    int(number_pages)
                )


            with col2:

                st.metric(
                    "Products collected",
                    len(live_df)
                )


            st.subheader(
                "Live scraping results"
            )


            st.dataframe(
                live_df,
                use_container_width=True
            )


            # --------------------------------
            # TELECHARGEMENT RESULTAT LIVE
            # --------------------------------

            live_csv = (
                live_df
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8"
                )
            )


            st.download_button(
                label=(
                    "⬇️ Download live "
                    "scraping result"
                ),

                data=live_csv,

                file_name=(
                    "live_books_scraping.csv"
                ),

                mime="text/csv"
            )


        except Exception as error:

            st.error(
                "An error occurred "
                "during scraping."
            )

            st.exception(error)


        finally:

            if driver is not None:

                driver.quit()

                driver.quit()
