"""
AgriData Explorer: Understanding Indian Agriculture with EDA
--------------------------------------------------------------
A Streamlit dashboard that replaces the Power BI portion of the
"AgriData Explorer" project brief with an interactive Python dashboard.

Data source : ICRISAT-District_Level_Data.xlsx
Run with   : streamlit run agridata_explorer_app.py

Make sure ICRISAT-District_Level_Data.xlsx sits in the SAME FOLDER as this
script (or update DATA_PATH below).
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------------------
# 0. PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="AgriData Explorer",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = "ICRISAT-District_Level_Data.xlsx"

# ----------------------------------------------------------------------
# 1. DATA LOADING & CLEANING
# ----------------------------------------------------------------------
# Every crop that has AREA / PRODUCTION / YIELD triplets in the dataset.
CROPS = {
    "Rice": ("RICE AREA (1000 ha)", "RICE PRODUCTION (1000 tons)", "RICE YIELD (Kg per ha)"),
    "Wheat": ("WHEAT AREA (1000 ha)", "WHEAT PRODUCTION (1000 tons)", "WHEAT YIELD (Kg per ha)"),
    "Kharif Sorghum": ("KHARIF SORGHUM AREA (1000 ha)", "KHARIF SORGHUM PRODUCTION (1000 tons)", "KHARIF SORGHUM YIELD (Kg per ha)"),
    "Rabi Sorghum": ("RABI SORGHUM AREA (1000 ha)", "RABI SORGHUM PRODUCTION (1000 tons)", "RABI SORGHUM YIELD (Kg per ha)"),
    "Sorghum": ("SORGHUM AREA (1000 ha)", "SORGHUM PRODUCTION (1000 tons)", "SORGHUM YIELD (Kg per ha)"),
    "Pearl Millet": ("PEARL MILLET AREA (1000 ha)", "PEARL MILLET PRODUCTION (1000 tons)", "PEARL MILLET YIELD (Kg per ha)"),
    "Maize": ("MAIZE AREA (1000 ha)", "MAIZE PRODUCTION (1000 tons)", "MAIZE YIELD (Kg per ha)"),
    "Finger Millet": ("FINGER MILLET AREA (1000 ha)", "FINGER MILLET PRODUCTION (1000 tons)", "FINGER MILLET YIELD (Kg per ha)"),
    "Barley": ("BARLEY AREA (1000 ha)", "BARLEY PRODUCTION (1000 tons)", "BARLEY YIELD (Kg per ha)"),
    "Chickpea": ("CHICKPEA AREA (1000 ha)", "CHICKPEA PRODUCTION (1000 tons)", "CHICKPEA YIELD (Kg per ha)"),
    "Pigeonpea": ("PIGEONPEA AREA (1000 ha)", "PIGEONPEA PRODUCTION (1000 tons)", "PIGEONPEA YIELD (Kg per ha)"),
    "Minor Pulses": ("MINOR PULSES AREA (1000 ha)", "MINOR PULSES PRODUCTION (1000 tons)", "MINOR PULSES YIELD (Kg per ha)"),
    "Groundnut": ("GROUNDNUT AREA (1000 ha)", "GROUNDNUT PRODUCTION (1000 tons)", "GROUNDNUT YIELD (Kg per ha)"),
    "Sesamum": ("SESAMUM AREA (1000 ha)", "SESAMUM PRODUCTION (1000 tons)", "SESAMUM YIELD (Kg per ha)"),
    "Rapeseed & Mustard": ("RAPESEED AND MUSTARD AREA (1000 ha)", "RAPESEED AND MUSTARD PRODUCTION (1000 tons)", "RAPESEED AND MUSTARD YIELD (Kg per ha)"),
    "Safflower": ("SAFFLOWER AREA (1000 ha)", "SAFFLOWER PRODUCTION (1000 tons)", "SAFFLOWER YIELD (Kg per ha)"),
    "Castor": ("CASTOR AREA (1000 ha)", "CASTOR PRODUCTION (1000 tons)", "CASTOR YIELD (Kg per ha)"),
    "Linseed": ("LINSEED AREA (1000 ha)", "LINSEED PRODUCTION (1000 tons)", "LINSEED YIELD (Kg per ha)"),
    "Sunflower": ("SUNFLOWER AREA (1000 ha)", "SUNFLOWER PRODUCTION (1000 tons)", "SUNFLOWER YIELD (Kg per ha)"),
    "Soybean": ("SOYABEAN AREA (1000 ha)", "SOYABEAN PRODUCTION (1000 tons)", "SOYABEAN YIELD (Kg per ha)"),
    "Oilseeds": ("OILSEEDS AREA (1000 ha)", "OILSEEDS PRODUCTION (1000 tons)", "OILSEEDS YIELD (Kg per ha)"),
    "Sugarcane": ("SUGARCANE AREA (1000 ha)", "SUGARCANE PRODUCTION (1000 tons)", "SUGARCANE YIELD (Kg per ha)"),
    "Cotton": ("COTTON AREA (1000 ha)", "COTTON PRODUCTION (1000 tons)", "COTTON YIELD (Kg per ha)"),
}

AREA_ONLY_COLS = [
    "FRUITS AREA (1000 ha)", "VEGETABLES AREA (1000 ha)",
    "FRUITS AND VEGETABLES AREA (1000 ha)", "POTATOES AREA (1000 ha)",
    "ONION AREA (1000 ha)", "FODDER AREA (1000 ha)",
]


@st.cache_data(show_spinner="Loading & cleaning ICRISAT dataset...")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    # --- Cleaning -------------------------------------------------
    # ICRISAT uses -1 as a "missing / not recorded" sentinel value.
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for c in ["Dist Code", "Year", "State Code"]:
        if c in numeric_cols:
            numeric_cols.remove(c)
    df[numeric_cols] = df[numeric_cols].mask(df[numeric_cols] < 0)

    # Strip whitespace / standardize text fields
    for c in ["State Name", "Dist Name"]:
        df[c] = df[c].astype(str).str.strip()

    df["Year"] = df["Year"].astype(int)
    return df


def crop_cols(crop_name):
    return CROPS[crop_name]


# ----------------------------------------------------------------------
# 2. LOAD DATA (with friendly error if file missing)
# ----------------------------------------------------------------------
if not os.path.exists(DATA_PATH):
    st.error(
        f"Could not find **{DATA_PATH}**. Place the ICRISAT-District_Level_Data.xlsx "
        "file in the same folder as this script, or edit DATA_PATH at the top of the file."
    )
    st.stop()

df = load_data(DATA_PATH)
YEAR_MIN, YEAR_MAX = int(df["Year"].min()), int(df["Year"].max())
ALL_STATES = sorted(df["State Name"].unique())

# ----------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# ----------------------------------------------------------------------
st.sidebar.title("🌾 AgriData Explorer")
page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Overview",
        "🧹 Data Cleaning Summary",
        "📊 EDA Explorer",
        "🧠 SQL-Style Insights (Q1–Q10)",
        "🌱 Crop Recommendation Helper",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data: ICRISAT District Level Data (1966–2017) · "
    "Values of -1 in the source file are treated as missing and excluded."
)

# ----------------------------------------------------------------------
# 4. PAGE: OVERVIEW
# ----------------------------------------------------------------------
if page == "🏠 Overview":
    st.title("🌾 AgriData Explorer")
    st.subheader("Understanding Indian Agriculture with EDA — Streamlit Edition")

    st.markdown(
        """
        This dashboard replaces the Power BI deliverable from the project brief with an
        interactive **Streamlit + Plotly** application. It covers:

        - **Data cleaning** of the ICRISAT district-level dataset
        - **Exploratory Data Analysis (EDA)** — the full list of charts requested in the brief
        - **The 10 analytical questions** the project asks you to answer
        - A simple **crop recommendation helper** for a chosen district
        """
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Districts", df["Dist Name"].nunique())
    c2.metric("States", df["State Name"].nunique())
    c3.metric("Years covered", f"{YEAR_MIN}–{YEAR_MAX}")
    c4.metric("Records", f"{len(df):,}")

    st.markdown("### Total Rice vs Wheat Production Over Time (All-India)")
    trend = df.groupby("Year")[["RICE PRODUCTION (1000 tons)", "WHEAT PRODUCTION (1000 tons)"]].sum().reset_index()
    fig = px.line(
        trend, x="Year", y=["RICE PRODUCTION (1000 tons)", "WHEAT PRODUCTION (1000 tons)"],
        labels={"value": "Production (1000 tons)", "variable": "Crop"},
        title="India's Rice & Wheat Production Trend",
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------
# 5. PAGE: DATA CLEANING SUMMARY
# ----------------------------------------------------------------------
elif page == "🧹 Data Cleaning Summary":
    st.title("🧹 Data Cleaning Summary")

    st.markdown(
        """
        **Steps applied** (mirrors the brief's "Data Collection and Cleaning" section):

        1. Loaded the raw ICRISAT district-level Excel file.
        2. Replaced the dataset's `-1` "not recorded" sentinel with `NaN` across all
           AREA / PRODUCTION / YIELD columns, so they don't distort averages or sums.
        3. Trimmed whitespace from `State Name` and `Dist Name`.
        4. Cast `Year` to integer for correct time-series ordering.
        5. Units are already standardized by ICRISAT: Area = 1000 ha, Production = 1000 tons,
           Yield = Kg/ha — no further unit conversion needed.
        """
    )

    raw = pd.read_excel(DATA_PATH)
    missing_raw = int((raw.select_dtypes(include=[np.number]) < 0).sum().sum())
    missing_clean = int(df.isna().sum().sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Raw rows", f"{len(raw):,}")
    c1.metric("Raw columns", raw.shape[1])
    c2.metric("Sentinel (-1) values found", f"{missing_raw:,}")
    c3.metric("NaN values after cleaning", f"{missing_clean:,}")

    st.markdown("### Missing values by column (top 15, cleaned data)")
    na_counts = df.isna().sum().sort_values(ascending=False).head(15)
    fig = px.bar(na_counts, orientation="h", labels={"value": "Missing count", "index": "Column"},
                 title="Columns with the most missing data")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Preview of cleaned data")
    st.dataframe(df.head(50), use_container_width=True)

# ----------------------------------------------------------------------
# 6. PAGE: EDA EXPLORER
# ----------------------------------------------------------------------
elif page == "📊 EDA Explorer":
    st.title("📊 Exploratory Data Analysis")
    st.caption("Every chart from the project brief's EDA checklist, made interactive.")

    eda_choice = st.selectbox(
        "Choose an analysis",
        [
            "Top 7 Rice Production States",
            "Top 5 Wheat Producing States (+ share %)",
            "Oilseed Production by Top 5 States",
            "Top 7 Sunflower Production States",
            "India's Sugarcane Production — Last 50 Years",
            "Rice vs Wheat Production — Last 50 Years",
            "Rice Production by West Bengal Districts",
            "Top 10 Wheat Production Years from Uttar Pradesh",
            "Millet Production (Pearl + Finger) — Last 50 Years",
            "Sorghum Production (Kharif vs Rabi) by Region",
            "Top 7 States for Groundnut Production",
            "Soybean Production by Top 5 States & Yield Efficiency",
            "Oilseed Production in Major States",
            "Impact of Area Cultivated on Production (Rice/Wheat/Maize)",
            "Rice vs Wheat Yield Across States",
        ],
    )

    if eda_choice == "Top 7 Rice Production States":
        agg = df.groupby("State Name")["RICE PRODUCTION (1000 tons)"].sum().nlargest(7).reset_index()
        fig = px.bar(agg, x="State Name", y="RICE PRODUCTION (1000 tons)", color="State Name",
                     title="Top 7 Rice Producing States (total 1966–2017)")
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Top 5 Wheat Producing States (+ share %)":
        agg = df.groupby("State Name")["WHEAT PRODUCTION (1000 tons)"].sum().nlargest(5).reset_index()
        c1, c2 = st.columns(2)
        fig1 = px.bar(agg, x="State Name", y="WHEAT PRODUCTION (1000 tons)", color="State Name",
                      title="Top 5 Wheat Producing States")
        fig2 = px.pie(agg, names="State Name", values="WHEAT PRODUCTION (1000 tons)",
                      title="Share of Top 5 Wheat States")
        c1.plotly_chart(fig1, use_container_width=True)
        c2.plotly_chart(fig2, use_container_width=True)

    elif eda_choice == "Oilseed Production by Top 5 States":
        agg = df.groupby("State Name")["OILSEEDS PRODUCTION (1000 tons)"].sum().nlargest(5).reset_index()
        fig = px.bar(agg, x="State Name", y="OILSEEDS PRODUCTION (1000 tons)", color="State Name",
                     title="Top 5 Oilseed Producing States")
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Top 7 Sunflower Production States":
        agg = df.groupby("State Name")["SUNFLOWER PRODUCTION (1000 tons)"].sum().nlargest(7).reset_index()
        fig = px.bar(agg, x="State Name", y="SUNFLOWER PRODUCTION (1000 tons)", color="State Name",
                     title="Top 7 Sunflower Producing States")
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "India's Sugarcane Production — Last 50 Years":
        agg = df.groupby("Year")["SUGARCANE PRODUCTION (1000 tons)"].sum().reset_index()
        fig = px.line(agg, x="Year", y="SUGARCANE PRODUCTION (1000 tons)",
                      title="India's Sugarcane Production, Last 50 Years", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Rice vs Wheat Production — Last 50 Years":
        agg = df.groupby("Year")[["RICE PRODUCTION (1000 tons)", "WHEAT PRODUCTION (1000 tons)"]].sum().reset_index()
        fig = px.line(agg, x="Year", y=["RICE PRODUCTION (1000 tons)", "WHEAT PRODUCTION (1000 tons)"],
                      title="Rice vs Wheat Production, Last 50 Years")
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Rice Production by West Bengal Districts":
        wb = df[df["State Name"] == "West Bengal"]
        agg = wb.groupby("Dist Name")["RICE PRODUCTION (1000 tons)"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(agg, x="Dist Name", y="RICE PRODUCTION (1000 tons)",
                     title="Rice Production by West Bengal District (total)")
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Top 10 Wheat Production Years from Uttar Pradesh":
        up = df[df["State Name"] == "Uttar Pradesh"]
        agg = up.groupby("Year")["WHEAT PRODUCTION (1000 tons)"].sum().nlargest(10).reset_index()
        fig = px.bar(agg.sort_values("Year"), x="Year", y="WHEAT PRODUCTION (1000 tons)",
                     title="Top 10 Wheat Production Years — Uttar Pradesh")
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Millet Production (Pearl + Finger) — Last 50 Years":
        tmp = df.copy()
        tmp["MILLET PRODUCTION (1000 tons)"] = (
            tmp["PEARL MILLET PRODUCTION (1000 tons)"].fillna(0)
            + tmp["FINGER MILLET PRODUCTION (1000 tons)"].fillna(0)
        )
        agg = tmp.groupby("Year")["MILLET PRODUCTION (1000 tons)"].sum().reset_index()
        fig = px.line(agg, x="Year", y="MILLET PRODUCTION (1000 tons)",
                      title="India's Millet (Pearl + Finger) Production, Last 50 Years", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Sorghum Production (Kharif vs Rabi) by Region":
        agg = df.groupby("State Name")[
            ["KHARIF SORGHUM PRODUCTION (1000 tons)", "RABI SORGHUM PRODUCTION (1000 tons)"]
        ].sum()
        agg = agg[(agg.T != 0).any()].reset_index()
        fig = px.bar(agg, x="State Name", y=["KHARIF SORGHUM PRODUCTION (1000 tons)", "RABI SORGHUM PRODUCTION (1000 tons)"],
                     barmode="group", title="Kharif vs Rabi Sorghum Production by State")
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Top 7 States for Groundnut Production":
        agg = df.groupby("State Name")["GROUNDNUT PRODUCTION (1000 tons)"].sum().nlargest(7).reset_index()
        fig = px.bar(agg, x="State Name", y="GROUNDNUT PRODUCTION (1000 tons)", color="State Name",
                     title="Top 7 Groundnut Producing States")
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Soybean Production by Top 5 States & Yield Efficiency":
        agg = df.groupby("State Name").agg(
            production=("SOYABEAN PRODUCTION (1000 tons)", "sum"),
            avg_yield=("SOYABEAN YIELD (Kg per ha)", "mean"),
        ).nlargest(5, "production").reset_index()
        c1, c2 = st.columns(2)
        fig1 = px.bar(agg, x="State Name", y="production", color="State Name", title="Top 5 Soybean States — Production")
        fig2 = px.bar(agg, x="State Name", y="avg_yield", color="State Name", title="Avg Soybean Yield (Kg/ha)")
        c1.plotly_chart(fig1, use_container_width=True)
        c2.plotly_chart(fig2, use_container_width=True)

    elif eda_choice == "Oilseed Production in Major States":
        agg = df.groupby("State Name")["OILSEEDS PRODUCTION (1000 tons)"].sum().nlargest(10).reset_index()
        fig = px.bar(agg, x="OILSEEDS PRODUCTION (1000 tons)", y="State Name", orientation="h",
                     title="Oilseed Production — Major States")
        st.plotly_chart(fig, use_container_width=True)

    elif eda_choice == "Impact of Area Cultivated on Production (Rice/Wheat/Maize)":
        crop_pick = st.radio("Crop", ["Rice", "Wheat", "Maize"], horizontal=True)
        a_col, p_col, _ = crop_cols(crop_pick)
        sample = df[[a_col, p_col, "State Name"]].dropna()
        fig = px.scatter(sample, x=a_col, y=p_col, color="State Name", opacity=0.6, trendline="ols",
                          title=f"{crop_pick}: Area Cultivated vs Production (district-years)")
        st.plotly_chart(fig, use_container_width=True)
        corr = sample[[a_col, p_col]].corr().iloc[0, 1]
        st.info(f"Correlation between area and production for {crop_pick}: **{corr:.3f}**")

    elif eda_choice == "Rice vs Wheat Yield Across States":
        agg = df.groupby("State Name")[["RICE YIELD (Kg per ha)", "WHEAT YIELD (Kg per ha)"]].mean().reset_index()
        fig = px.bar(agg, x="State Name", y=["RICE YIELD (Kg per ha)", "WHEAT YIELD (Kg per ha)"],
                     barmode="group", title="Average Rice vs Wheat Yield by State")
        st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------
# 7. PAGE: SQL-STYLE INSIGHTS (the 10 questions from the brief)
# ----------------------------------------------------------------------
elif page == "🧠 SQL-Style Insights (Q1–Q10)":
    st.title("🧠 The 10 Analytical Questions")
    st.caption("Answered with pandas (equivalent SQL logic shown for each) instead of raw SQL, and visualized directly.")

    q = st.selectbox(
        "Pick a question",
        [
            "Q1. Year-wise Trend of Rice Production Across States (Top 3)",
            "Q2. Top 5 Districts by Wheat Yield Increase Over the Last 5 Years",
            "Q3. States with the Highest Growth in Oilseed Production (5-Year Growth Rate)",
            "Q4. District-wise Correlation Between Area & Production (Rice, Wheat, Maize)",
            "Q5. Yearly Production Growth of Cotton in Top 5 Cotton Producing States",
            "Q6. Districts with the Highest Groundnut Production in 2017",
            "Q7. Annual Average Maize Yield Across All States",
            "Q8. Total Area Cultivated for Oilseeds in Each State",
            "Q9. Districts with the Highest Rice Yield",
            "Q10. Compare Production of Wheat and Rice for Top 5 States Over 10 Years",
        ],
    )

    if q.startswith("Q1."):
        top3 = df.groupby("State Name")["RICE PRODUCTION (1000 tons)"].sum().nlargest(3).index.tolist()
        sub = df[df["State Name"].isin(top3)]
        agg = sub.groupby(["Year", "State Name"])["RICE PRODUCTION (1000 tons)"].sum().reset_index()
        fig = px.line(agg, x="Year", y="RICE PRODUCTION (1000 tons)", color="State Name",
                      title=f"Year-wise Rice Production — Top 3 States ({', '.join(top3)})")
        st.plotly_chart(fig, use_container_width=True)

    elif q.startswith("Q2."):
        last5 = sorted(df["Year"].unique())[-5:]
        sub = df[df["Year"].isin([last5[0], last5[-1]])]
        piv = sub.pivot_table(index=["State Name", "Dist Name"], columns="Year",
                               values="WHEAT YIELD (Kg per ha)")
        piv = piv.dropna()
        piv["increase"] = piv[last5[-1]] - piv[last5[0]]
        top5 = piv.nlargest(5, "increase").reset_index()
        st.write(f"Comparing yield in **{last5[0]}** vs **{last5[-1]}**")
        fig = px.bar(top5, x="Dist Name", y="increase", color="State Name",
                     title="Top 5 Districts by Wheat Yield Increase (Kg/ha)")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top5, use_container_width=True)

    elif q.startswith("Q3."):
        last5 = sorted(df["Year"].unique())[-5:]
        sub = df[df["Year"].isin([last5[0], last5[-1]])]
        agg = sub.groupby(["State Name", "Year"])["OILSEEDS PRODUCTION (1000 tons)"].sum().unstack()
        agg = agg.dropna()
        agg["growth_%"] = ((agg[last5[-1]] - agg[last5[0]]) / agg[last5[0]].replace(0, np.nan)) * 100
        top = agg.sort_values("growth_%", ascending=False).head(10).reset_index()
        fig = px.bar(top, x="State Name", y="growth_%", color="State Name",
                     title=f"Oilseed Production Growth % ({last5[0]} → {last5[-1]})")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top, use_container_width=True)

    elif q.startswith("Q4."):
        crop_pick = st.radio("Crop", ["Rice", "Wheat", "Maize"], horizontal=True, key="q4crop")
        a_col, p_col, _ = crop_cols(crop_pick)
        dist_corr = (
            df.dropna(subset=[a_col, p_col])
            .groupby(["State Name", "Dist Name"])
            .apply(lambda g: g[a_col].corr(g[p_col]) if len(g) > 2 else np.nan)
            .dropna()
            .reset_index(name="correlation")
        )
        st.dataframe(dist_corr.sort_values("correlation", ascending=False), use_container_width=True)
        fig = px.histogram(dist_corr, x="correlation", nbins=30,
                            title=f"Distribution of District-wise Area↔Production Correlation — {crop_pick}")
        st.plotly_chart(fig, use_container_width=True)

    elif q.startswith("Q5."):
        top5cotton = df.groupby("State Name")["COTTON PRODUCTION (1000 tons)"].sum().nlargest(5).index.tolist()
        sub = df[df["State Name"].isin(top5cotton)]
        agg = sub.groupby(["Year", "State Name"])["COTTON PRODUCTION (1000 tons)"].sum().reset_index()
        fig = px.line(agg, x="Year", y="COTTON PRODUCTION (1000 tons)", color="State Name",
                      title=f"Yearly Cotton Production Growth — Top 5 States ({', '.join(top5cotton)})")
        st.plotly_chart(fig, use_container_width=True)

    elif q.startswith("Q6."):
        sub = df[df["Year"] == 2017]
        top = sub.groupby(["State Name", "Dist Name"])["GROUNDNUT PRODUCTION (1000 tons)"].sum().nlargest(10).reset_index()
        fig = px.bar(top, x="Dist Name", y="GROUNDNUT PRODUCTION (1000 tons)", color="State Name",
                     title="Top Districts — Groundnut Production in 2017")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top, use_container_width=True)

    elif q.startswith("Q7."):
        agg = df.groupby("Year")["MAIZE YIELD (Kg per ha)"].mean().reset_index()
        fig = px.line(agg, x="Year", y="MAIZE YIELD (Kg per ha)", markers=True,
                      title="Annual Average Maize Yield Across All States")
        st.plotly_chart(fig, use_container_width=True)

    elif q.startswith("Q8."):
        agg = df.groupby("State Name")["OILSEEDS AREA (1000 ha)"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(agg, x="State Name", y="OILSEEDS AREA (1000 ha)", color="State Name",
                     title="Total Area Cultivated for Oilseeds by State")
        st.plotly_chart(fig, use_container_width=True)

    elif q.startswith("Q9."):
        agg = df.groupby(["State Name", "Dist Name"])["RICE YIELD (Kg per ha)"].mean().nlargest(15).reset_index()
        fig = px.bar(agg, x="Dist Name", y="RICE YIELD (Kg per ha)", color="State Name",
                     title="Districts with the Highest Average Rice Yield (top 15)")
        st.plotly_chart(fig, use_container_width=True)

    elif q.startswith("Q10."):
        top5 = df.groupby("State Name")["RICE PRODUCTION (1000 tons)"].sum().nlargest(5).index.tolist()
        last10 = sorted(df["Year"].unique())[-10:]
        sub = df[(df["State Name"].isin(top5)) & (df["Year"].isin(last10))]
        agg = sub.groupby(["Year", "State Name"])[["RICE PRODUCTION (1000 tons)", "WHEAT PRODUCTION (1000 tons)"]].sum().reset_index()
        c1, c2 = st.columns(2)
        fig1 = px.line(agg, x="Year", y="RICE PRODUCTION (1000 tons)", color="State Name", title="Rice — Last 10 Years")
        fig2 = px.line(agg, x="Year", y="WHEAT PRODUCTION (1000 tons)", color="State Name", title="Wheat — Last 10 Years")
        c1.plotly_chart(fig1, use_container_width=True)
        c2.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------------------------
# 8. PAGE: CROP RECOMMENDATION HELPER
# ----------------------------------------------------------------------
elif page == "🌱 Crop Recommendation Helper":
    st.title("🌱 Crop Recommendation Helper")
    st.caption("A simple, transparent rule-based helper (stand-in for the brief's 'Advanced Analytics' section).")

    state_pick = st.selectbox("State", ALL_STATES)
    dists = sorted(df.loc[df["State Name"] == state_pick, "Dist Name"].unique())
    dist_pick = st.selectbox("District", dists)

    dsub = df[(df["State Name"] == state_pick) & (df["Dist Name"] == dist_pick)]

    rows = []
    for crop, (a_col, p_col, y_col) in CROPS.items():
        yield_series = dsub[y_col].dropna()
        if len(yield_series) >= 3:
            rows.append({
                "Crop": crop,
                "Avg Yield (Kg/ha)": yield_series.mean(),
                "Yield Trend (last-first)": yield_series.iloc[-1] - yield_series.iloc[0] if len(yield_series) > 1 else 0,
                "Years of data": len(yield_series),
            })
    rec_df = pd.DataFrame(rows).sort_values("Avg Yield (Kg/ha)", ascending=False)

    if rec_df.empty:
        st.warning("Not enough historical yield data for this district to make a recommendation.")
    else:
        st.markdown(f"### Historical crop performance in **{dist_pick}, {state_pick}**")
        st.dataframe(rec_df, use_container_width=True)

        best = rec_df.iloc[0]
        st.success(
            f"Based on historical average yield, **{best['Crop']}** has performed best in this district "
            f"(avg {best['Avg Yield (Kg/ha)']:.0f} Kg/ha across {int(best['Years of data'])} recorded years)."
        )

        fig = px.bar(rec_df.head(10), x="Crop", y="Avg Yield (Kg/ha)", color="Crop",
                     title=f"Top Crops by Average Yield — {dist_pick}")
        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Note: this is a simple descriptive ranking based on historical yield averages, "
            "not a predictive machine-learning model. It's meant to illustrate the kind of "
            "recommendation the full 'Advanced Analytics' step in the brief describes."
        )
