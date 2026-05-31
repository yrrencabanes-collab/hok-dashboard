import streamlit as st
from core.scouting_ai import ScoutingAI
from core.draft_forecaster import DraftForecaster
from core.counter_ai import CounterDraftAI

st.title("🧠 AI Esports Scouting System — Systemic Chaos")

enemy_team = st.text_input("Enter Enemy Team Name")

if st.button("Run Full Scouting Analysis"):

    scouting = ScoutingAI(df)
    forecaster = DraftForecaster(scouting, hero_df)
    counter_ai = CounterDraftAI()

    st.subheader("🔍 Enemy Identity Profile")
    st.write(scouting.team_identity_profile(enemy_team))

    st.subheader("⚔️ Predicted Enemy Draft")
    st.json(forecaster.predict_full_draft(enemy_team))

    st.subheader("🧠 Counter Draft Suggestions")
    st.dataframe(counter_ai.generate_counter_draft([], hero_df))
