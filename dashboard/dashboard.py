import duckdb
import pandas as pd
import streamlit as st
import altair as alt
from pathlib import Path

# Resolve project root automatically
ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "local_datahub.duckdb"


# Title
st.title("📊 NBP Currency Analytics Dashboard")

st.markdown("""
Interaktywny dashboard analityczny oparty o dane z **NBP API**,
przetwarzane przez pipeline (Extract → Transform → Load → DuckDB → S3).
""")

# Load data
conn = duckdb.connect(str(DB_PATH))
df = conn.execute("SELECT * FROM nbp_rates ORDER BY effective_date").df()

# Sidebar filters
currency_options = df["code"].unique().tolist()
selected_currency = st.sidebar.selectbox("Wybierz walutę:", currency_options)

# Filtered data
df_cur = df[df["code"] == selected_currency]

st.header(f"📈 Trend kursu: {selected_currency}")

line_chart = alt.Chart(df_cur).mark_line().encode(
    x="effective_date:T",
    y="mid:Q",
    tooltip=["effective_date", "mid"]
).interactive()

st.altair_chart(line_chart, use_container_width=True)


# Volatility section
st.header(f"📉 Dzienne zmiany (%): {selected_currency}")

df_cur["pct_change"] = df_cur["mid"].pct_change() * 100

vol_chart = alt.Chart(df_cur.dropna()).mark_bar().encode(
    x="effective_date:T",
    y="pct_change:Q",
    tooltip=["effective_date", "pct_change"]
).interactive()

st.altair_chart(vol_chart, use_container_width=True)


# Summary statistics
st.header("📘 Statystyki")

st.write(df_cur.describe()[["mid"]])

# Heatmap of currencies
st.header("🔥 Heatmapa korelacji między walutami")

pivot = df.pivot_table(index="effective_date", columns="code", values="mid")
corr = pivot.corr()

heatmap = alt.Chart(
    corr.reset_index().melt("code")
).mark_rect().encode(
    x="code:N",
    y="variable:N",
    color="value:Q",
    tooltip=["code", "variable", "value"]
)

st.altair_chart(heatmap, use_container_width=True)
