import streamlit as st
import pandas as pd

st.set_page_config(page_title="Input Scrimmage Stats", page_icon="📝", layout="wide")

st.title("📝 Post-Scrimmage Report Form")
st.markdown("Input game telemetry data immediately after blocks end to keep trends updated.")

# Input Form
with st.form("scrim_report_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        date = st.date_input("Match Date")
        opponent = st.text_input("Opponent Name", placeholder="e.g. Cloud9")
        map_mode = st.text_input("Map / Game Mode", placeholder="e.g. Bind / Hardpoint")
        
    with col2:
        result = st.radio("Outcome", ["Win", "Loss", "Tie"], horizontal=True)
        team_score = st.number_input("Your Team Score", min_value=0, step=1, value=0)
        opp_score = st.number_input("Opponent Team Score", min_value=0, step=1, value=0)
        
    with col3:
        notes = st.text_area("Coach Performance Notes", placeholder="Note down ultimate economy issues, map control, or setup breakdowns...")

    submit_button = st.form_submit_button("Submit Game Report")

if submit_button:
    if opponent and map_mode:
        # Create a new row dataframe
        new_data = pd.DataFrame([{
            "Date": str(date),
            "Opponent": opponent,
            "Map/Mode": map_mode,
            "Result": result,
            "Team_Score": int(team_score),
            "Opp_Score": int(opp_score),
            "Notes": notes
        }])
        
        # Append data to global session state
        st.session_state.scrim_results = pd.concat([st.session_state.scrim_results, new_data], ignore_index=True)
        st.success("Scrim results securely saved into session memory!")
    else:
        st.error("Missing fields: Please make sure 'Opponent' and 'Map/Mode' are filled out.")

st.divider()

# Display Live App Database Sheet
st.subheader("📊 Logged Scrim History (Current Session)")
st.dataframe(st.session_state.scrim_results, use_container_width=True, hide_index=True)
