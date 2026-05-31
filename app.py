import streamlit as pd
import streamlit as st
import pandas as pd

# Page Configuration for Responsive Layout
st.set_page_config(
    page_title="Esports Coach Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"  # <-- This forces it open on load
)

# Initialize Session State Data if it doesn't exist
if 'players' not in st.session_state:
    st.session_state.players = {
        "Player 1 (IGL)": {"K/D": 1.2, "Win Rate": "62%", "Most Played": "Agent A/Hero A", "Form": "🔥 Up"},
        "Player 2 (Entry)": {"K/D": 1.4, "Win Rate": "58%", "Most Played": "Agent B/Hero B", "Form": "稳定 Stable"},
        "Player 3 (Support)": {"K/D": 0.9, "Win Rate": "65%", "Most Played": "Agent C/Hero C", "Form": "🔥 Up"},
        "Player 4 (Flex)": {"K/D": 1.0, "Win Rate": "50%", "Most Played": "Agent D/Hero D", "Form": "📉 Down"},
        "Player 5 (Sniper)": {"K/D": 1.5, "Win Rate": "70%", "Most Played": "Agent E/Hero E", "Form": "🔥 Peak"}
    }

if 'scrims' not in st.session_state:
    st.session_state.scrims = [
        {"Date": "2026-06-01", "Time": "18:00", "Opponent": "Team Alpha", "Format": "BO3", "Status": "Scheduled"},
        {"Date": "2026-06-02", "Time": "20:00", "Opponent": "Team Liquid Echo", "Format": "BO5", "Status": "Pending Confirmation"},
    ]

if 'scrim_results' not in st.session_state:
    st.session_state.scrim_results = pd.DataFrame([
        {"Date": "2026-05-30", "Opponent": "Fnatic Academy", "Map/Mode": "Map 1", "Result": "Win", "Team_Score": 13, "Opp_Score": 9, "Notes": "Good communication on eco rounds."},
        {"Date": "2026-05-30", "Opponent": "Fnatic Academy", "Map/Mode": "Map 2", "Result": "Loss", "Team_Score": 8, "Opp_Score": 13, "Notes": "Mid-game rotations were too slow."}
    ])

# Header Section
st.title("🎮 Esports Coach Command Center")
st.markdown("Welcome coach! Monitor player growth, manage upcoming schedules, and log live scrimmage metrics.")

st.divider()

# High-Level Metrics Grid
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Overall Scrim Win Rate", value="55.6%", delta="+3.2% vs last week")
with col2:
    st.metric(label="Active Roster", value="5 Players", delta="Healthy")
with col3:
    st.metric(label="Next Scheduled Scrim", value="June 1st, 18:00", delta="vs Team Alpha")

st.markdown("### 📋 Navigation Guide")
st.info("Use the **Sidebar menu** on the left to navigate between different tracking pages. If you are on a mobile device, tap the **>** arrow in the top-left corner to open the menu.")
