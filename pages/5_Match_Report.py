import streamlit as st
import pandas as pd

st.title("📁 Match History")

data = pd.DataFrame({
    "Opponent": ["Team A", "Team B", "Team C"],
    "Result": ["Win", "Loss", "Win"],
    "Duration": ["18:10", "22:05", "19:45"]
})

st.dataframe(data, use_container_width=True)
