# football_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_football_stats.csv")

    # ✅ Clean potential issues (convert to string to avoid TypeError)
    df["Club"] = df["Club"].fillna("Unknown").astype(str)
    df["Position"] = df["Position"].fillna("Unknown").astype(str)
    df["Nationality"] = df["Nationality"].fillna("Unknown").astype(str)
    return df

df = load_data()

# ==============================
# SIDEBAR FILTERS
# ==============================
st.sidebar.header("⚽ Filter Players")

# Filter: Club
clubs = ["All"] + sorted(df["Club"].unique().tolist())
selected_club = st.sidebar.selectbox("Select Club", clubs)

# Filter: Position
positions = ["All"] + sorted(df["Position"].unique().tolist())
selected_position = st.sidebar.selectbox("Select Position", positions)

# Filter: Nationality
nations = ["All"] + sorted(df["Nationality"].unique().tolist())
selected_nation = st.sidebar.selectbox("Select Nationality", nations)

# ==============================
# APPLY FILTERS
# ==============================
filtered_df = df.copy()
if selected_club != "All":
    filtered_df = filtered_df[filtered_df["Club"] == selected_club]
if selected_position != "All":
    filtered_df = filtered_df[filtered_df["Position"] == selected_position]
if selected_nation != "All":
    filtered_df = filtered_df[filtered_df["Nationality"] == selected_nation]

# ==============================
# KPIs (Key Performance Indicators)
# ==============================
st.title("⚽ Football Stats Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Players", filtered_df["Name"].nunique())
col2.metric("Avg Age", round(filtered_df["Age"].mean(), 1))
col3.metric("Total Goals", int(filtered_df["Goals"].sum()))
col4.metric("Total Assists", int(filtered_df["Assists"].sum()))

# ==============================
# VISUALIZATIONS
# ==============================
st.subheader("📊 Goals by Club (Top 10)")
top_goals = (
    filtered_df.groupby("Club")["Goals"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig1 = px.bar(top_goals, x="Club", y="Goals", color="Goals", text="Goals")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Assists by Club (Top 10)")
top_assists = (
    filtered_df.groupby("Club")["Assists"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig2 = px.bar(top_assists, x="Club", y="Assists", color="Assists", text="Assists")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📊 Age Distribution")
fig3 = px.histogram(filtered_df, x="Age", nbins=20, color="Position")
st.plotly_chart(fig3, use_container_width=True)

# ==============================
# PLAYER TABLE
# ==============================
st.subheader("📋 Player Data")
st.dataframe(filtered_df)

# ==============================
# PLAYER COMPARISON
# ==============================
st.subheader("⚔️ Compare Two Players")

player_list = df["Name"].dropna().unique().tolist()
player1 = st.selectbox("Select First Player", player_list, index=0)
player2 = st.selectbox("Select Second Player", player_list, index=1)

if player1 and player2 and player1 != player2:
    p1 = df[df["Name"] == player1].iloc[0]
    p2 = df[df["Name"] == player2].iloc[0]

    st.write(f"### {player1} vs {player2}")

    # Create comparison table
    comparison_data = pd.DataFrame({
        "Metric": ["Age", "Club", "Position", "Nationality", "Goals", "Assists", "MarketValue"],
        player1: [p1["Age"], p1["Club"], p1["Position"], p1["Nationality"], p1["Goals"], p1["Assists"], p1.get("MarketValue", "N/A")],
        player2: [p2["Age"], p2["Club"], p2["Position"], p2["Nationality"], p2["Goals"], p2["Assists"], p2.get("MarketValue", "N/A")]
    })

    st.table(comparison_data)

    # Goals & Assists comparison chart
    fig_compare = px.bar(
        comparison_data[comparison_data["Metric"].isin(["Goals", "Assists"])],
        x="Metric", y=[player1, player2],
        barmode="group", text_auto=True
    )
    st.plotly_chart(fig_compare, use_container_width=True)


# === Descriptions for Dashboard ===

# KPI section
st.markdown("Here you can see the most important statistics from the filtered dataset — such as the total number of players and their average goals, assists, and market value.")

# Goals chart
st.markdown("This bar chart shows the **top 10 players with the highest goals**. It helps identify the most prolific goal scorers.")

# Assists chart
st.markdown("This chart highlights the **top 10 players with the most assists** — often the key playmakers in a team.")

# Market Value chart
st.markdown("This chart displays the **average market value per club**, giving an idea of which teams have the most expensive squads.")

# Discipline chart
st.markdown("The stacked bar chart shows the total **yellow and red cards by club**, providing insight into discipline and aggression levels of different teams.")


