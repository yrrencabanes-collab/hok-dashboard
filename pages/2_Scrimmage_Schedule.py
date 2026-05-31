import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scrimmage Schedule", page_icon="📅", layout="wide")

st.title("📅 Scrimmage Schedule Manager")

# Convert to Dataframe for display
df_scrims = pd.DataFrame(st.session_state.scrims)

st.markdown("### Upcoming Schedule")
st.dataframe(df_scrims, use_container_width=True, hide_index=True)

st.divider()

# Simple UI Action block to schedule a new match
st.subheader("➕ Quick Add Scrim")
with st.expander("Schedule a new block"):
    with st.form("schedule_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        date = col1.date_input("Date")
        time = col2.time_input("Time")
        opponent = col1.text_input("Opponent Team Name")
        fmt = col2.selectbox("Format", ["BO1", "BO3", "BO5", "Block (Blocks of 4 Maps)"])
        
        submit = st.form_submit_button("Add to Schedule")
        if submit:
            if opponent:
                st.session_state.scrims.append({
                    "Date": str(date),
                    "Time": str(time),
                    "Opponent": opponent,
                    "Format": fmt,
                    "Status": "Scheduled"
                })
                st.success(f"Successfully added scrim vs {opponent}!")
                st.rerun()
            else:
                st.error("Please enter an opponent name.")
