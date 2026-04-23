from __future__ import annotations

import logging
import os
import time

import pandas as pd
import plotly.express as px
import snowflake.connector
import streamlit as st
from config import get_snowflake_config
from snowflake.connector.errors import DatabaseError, OperationalError

logger = logging.getLogger(__name__)

_SF_CFG = get_snowflake_config()
SNOWFLAKE_LOGIN_TIMEOUT = _SF_CFG["login_timeout"]
SNOWFLAKE_NETWORK_TIMEOUT = _SF_CFG["network_timeout"]
SNOWFLAKE_MAX_RETRIES = _SF_CFG["max_retries"]
SNOWFLAKE_RETRY_BACKOFF = _SF_CFG["retry_backoff"]

st.set_page_config(page_title="Bookshop Analytics", layout="wide")
st.title("Dashboard Big Data - Bookshop")
st.caption("Visualisation des données WAREHOUSE et MARTS dans Snowflake")


def get_connection() -> snowflake.connector.SnowflakeConnection:
    """Open a Snowflake connection using env vars, stopping the app if any are missing."""
    required = [
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_DATABASE",
    ]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        st.warning(
            "Variables d'environnement manquantes pour Snowflake: "
            + ", ".join(missing)
        )
        st.stop()

    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        login_timeout=SNOWFLAKE_LOGIN_TIMEOUT,
        network_timeout=SNOWFLAKE_NETWORK_TIMEOUT,
    )


@st.cache_data(ttl=300)
def query_df(sql: str) -> pd.DataFrame:
    """Execute a Snowflake query and return results as a DataFrame, with retries."""
    last_error: Exception | None = None
    for attempt in range(1, SNOWFLAKE_MAX_RETRIES + 1):
        try:
            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(rows, columns=columns)
            finally:
                conn.close()
        except (OperationalError, DatabaseError) as exc:
            last_error = exc
            logger.warning(
                "Snowflake query failed (attempt %s/%s): %s",
                attempt, SNOWFLAKE_MAX_RETRIES, exc,
            )
            if attempt < SNOWFLAKE_MAX_RETRIES:
                time.sleep(SNOWFLAKE_RETRY_BACKOFF ** attempt)

    st.error(f"Échec de la requête Snowflake après {SNOWFLAKE_MAX_RETRIES} tentatives : {last_error}")
    st.stop()


obt_df = query_df(
    """
    select *
    from BOOKSHOP.MARTS.OBT_SALES
    order by vente_id
    """
)

factures_df = query_df(
    """
    select *
    from BOOKSHOP.WAREHOUSE.FACT_FACTURES
    order by id
    """
)

monthly_df = query_df(
    """
    select
        annees,
        mois,
        sum(qte) as qte_vendue,
        sum(pu * qte) as chiffre_affaires
    from BOOKSHOP.WAREHOUSE.FACT_VENTES
    group by annees, mois
    """
)

books_df = query_df(
    """
    select book_intitule, sum(qte_vendue) as qte_vendue
    from BOOKSHOP.WAREHOUSE.FACT_BOOKS_MOIS
    group by book_intitule
    order by qte_vendue desc
    """
)

customers_df = query_df(
    """
    select
        c.nom as customer_nom,
        sum(f.total_paid) as montant_paye
    from BOOKSHOP.WAREHOUSE.FACT_FACTURES f
    join BOOKSHOP.WAREHOUSE.DIM_CUSTOMERS c
      on f.customer_id = c.id
    group by c.nom
    order by montant_paye desc
    """
)

ordre_mois = [
    "janvier",
    "fevrier",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "aout",
    "septembre",
    "octobre",
    "novembre",
    "decembre",
]
monthly_df["MOIS"] = pd.Categorical(monthly_df["MOIS"], categories=ordre_mois, ordered=True)
monthly_df = monthly_df.sort_values(["ANNEES", "MOIS"])
monthly_df["PERIODE"] = monthly_df["ANNEES"].astype(str) + " - " + monthly_df["MOIS"].astype(str)

col1, col2, col3 = st.columns(3)
col1.metric("Nombre de ventes", int(obt_df["VENTE_ID"].nunique()))
col2.metric("Chiffre d'affaires", f"{factures_df['TOTAL_AMOUNT'].sum():,.2f}")
col3.metric("Montant payé", f"{factures_df['TOTAL_PAID'].sum():,.2f}")

st.subheader("Ventes par mois")
fig_month = px.bar(
    monthly_df,
    x="PERIODE",
    y="CHIFFRE_AFFAIRES",
    color="QTE_VENDUE",
    title="Chiffre d'affaires mensuel",
)
st.plotly_chart(fig_month, use_container_width=True)

st.subheader("Livres les plus vendus")
fig_books = px.pie(
    books_df,
    names="BOOK_INTITULE",
    values="QTE_VENDUE",
    title="Répartition des ventes par livre",
)
st.plotly_chart(fig_books, use_container_width=True)

st.subheader("Montants payés par client")
fig_customers = px.bar(
    customers_df,
    x="CUSTOMER_NOM",
    y="MONTANT_PAYE",
    title="Montant payé par client",
)
st.plotly_chart(fig_customers, use_container_width=True)

st.subheader("Aperçu de la table MARTS.OBT_SALES")
st.dataframe(obt_df, use_container_width=True)
