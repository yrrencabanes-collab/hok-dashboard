import streamlit as st
import pandas as pd

st.title("👥 Team Roster")

data = {
    "Player": ["Dex", "Shinvonn", "Naksu", "Niel", "Yzah", "Nowiii"],
    "Role": ["Analyst Coach", "Head Coach", "Gold Lane", "Mid Lane", "Jungle", "Roam"]
}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

st.success("Leadership Structure: Dex oversees analysis, Shinvonn handles coaching.")
