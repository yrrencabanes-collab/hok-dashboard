import streamlit as st
import pandas as pd
from core.ai_coach import AICoach

st.title("🧠 AI Draft Coach System")

df = pd.read_csv("data/heroes.csv")

coach = AICoach(df)

role = st.selectbox("Select Role", ["Gold Lane", "Mid Lane", "Jungle", "Roam", "Exp Lane"])

enemy = st.text_input("Enemy Composition (comma separated heroes)")

if st.button("Generate Draft Recommendation"):
    rec = coach.recommend_pick(role, enemy)
    st.write("🔥 Best Picks:")
    st.dataframe(rec)

if st.button("Counter Pick Suggestion"):
    counter = coach.counter_pick(enemy.split(",")[0])
    st.write("⚔️ Counter Options:")
    st.dataframe(counter)
