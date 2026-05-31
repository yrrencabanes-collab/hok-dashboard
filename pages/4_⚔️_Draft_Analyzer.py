import streamlit as st

st.title("⚔️ Draft & Ban Analyzer")

heroes = ["Arthur", "Lu Bu", "Diao Chan", "Sun Shangxiang", "Zilong"]

st.selectbox("Blue Side First Pick Priority", heroes)
st.selectbox("Red Side Counter Pick", heroes)

st.info("Draft recommendation system placeholder (AI module ready for upgrade)")
