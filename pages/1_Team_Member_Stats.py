import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Team Member Stats", page_icon="📈", layout="wide")

st.title("📈 Individual Player Analytics")

# Sidebar/Dropdown Selector
selected_player = st.selectbox("Select a Player to Analyze", list(st.session_state.players.keys()))
player_data = st.session_state.players[selected_player]

# Mobile Friendly Cards
col1, col2, col3, col4 = st.columns([1,1,1,1])
col1.metric("Lifetime K/D Ratio", player_data["K/D"])
col2.metric("Win Rate", player_data["Win Rate"])
col3.metric("Signature Pick", player_data["Most Played"])
col4.metric("Recent Performance", player_data["Form"])

st.divider()

st.subheader(f"Performance Trends: {selected_player}")

# Generate Interactive Mock Graph for Performance History
# Real-world use case: replace this with a database fetch
mock_perf_data = pd.DataFrame({
    'Match': [f'Scrim {i}' for i in range(1, 11)],
    'KAST % (Kill/Assist/Survive/Trade)': [70, 72, 68, 85, 90, 78, 82, 88, 81, 89],
    'Damage Per Round': [140, 135, 150, 165, 180, 155, 160, 175, 162, 185]
})

tab1, tab2 = st.tabs(["🎯 KAST % Consistency", "⚔️ Combat Output"])

with tab1:
    fig_kast = px.line(mock_perf_data, x='Match', y='KAST % (Kill/Assist/Survive/Trade)', markers=True, title="Recent Round Contribution Efficiency")
    st.plotly_chart(fig_kast, use_container_width=True)

with tab2:
    fig_dmg = px.bar(mock_perf_data, x='Match', y='Damage Per Round', color='Damage Per Round', title="Damage Distribution Trend")
    st.plotly_chart(fig_dmg, use_container_width=True)
