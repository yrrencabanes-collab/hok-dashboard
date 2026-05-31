import streamlit as st
import pandas as pd
from core.match_analyzer import MatchAnalyzer

st.title("🧾 AI Match Report Generator")

match = pd.read_csv("data/match_history.csv")

analyzer = MatchAnalyzer()

if st.button("Generate Report"):
    report, summary = analyzer.generate_report(match.iloc[-1])

    st.json(report)
    st.success(summary)
