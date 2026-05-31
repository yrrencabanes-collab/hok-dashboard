import streamlit as st
import pandas as pd
from core.meta_engine import MetaEngine

st.title("📊 Hero Meta Tracker")

df = pd.read_csv("data/heroes.csv")

meta = MetaEngine(df)

st.subheader("🔥 S-Tier Heroes")
st.dataframe(meta.get_s_tier())

st.subheader("📈 Trending Heroes")
st.dataframe(meta.trending_heroes())
