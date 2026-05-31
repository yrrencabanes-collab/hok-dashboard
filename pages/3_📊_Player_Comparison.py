import streamlit as st
import pandas as pd

st.title("📊 Player Performance Comparison")

players = ["Naksu", "Shinvonn", "Niel", "Yzah", "Nowiii"]

selected = st.multiselect("Select Players", players, default=players[:2])

stats = pd.DataFrame({
    "Player": players,
    "KDA": [4.2, 3.8, 5.1, 4.0, 4.5],
    "Kill Participation": [72, 68, 75, 70, 73],
    "Farm Efficiency": [88, 82, 90, 85, 87]
})

st.dataframe(stats[stats["Player"].isin(selected)], use_container_width=True)
