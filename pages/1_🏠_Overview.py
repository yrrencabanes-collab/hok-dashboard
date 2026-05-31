import streamlit as st

st.title("📊 Team Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Win Rate", "68%", "↑ 4%")
col2.metric("Average Game Time", "18:42", "↓ 1:10")
col3.metric("Objective Control", "74%", "↑ 6%")

st.divider()

st.subheader("Team Identity")
st.write("""
Systemic Chaos focuses on aggressive early-game tempo, objective control,
and coordinated teamfight execution.
""")
