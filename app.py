import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="HoK Global Analyst Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stHeading h1, h2, h3 { color: #38bdf8 !important; }
    .card { background-color: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

# --- MOCK DATA GENERATION (Database simulation) ---
@st.cache_data
def load_mock_data():
    # Heroes Database
    heroes = pd.DataFrame({
        "Hero": ["Lam", "Li Bai", "Gongsun Li", "Shangguan", "Lu Bu", "Allain", "Dolia", "Kui", "Yaria"],
        "Role": ["Assassin", "Assassin", "Marksman", "Mage", "Clash", "Clash", "Support", "Support", "Support"],
        "Win_Rate": [52.4, 48.5, 53.1, 51.2, 47.8, 50.5, 54.2, 49.1, 51.8],
        "Ban_Rate": [65.2, 12.4, 45.0, 38.9, 5.2, 22.1, 70.4, 15.3, 33.2],
        "Counter_Pick": ["Dolia", "Lu Bu", "Kui", "Lam", "Gongsun Li", "Shangguan", "Lam", "Gongsun Li", "Dolia"],
        "Image_Url": [
            "https://api.dicebear.com/7.x/bottts/svg?seed=Lam", "https://api.dicebear.com/7.x/bottts/svg?seed=LiBai",
            "https://api.dicebear.com/7.x/bottts/svg?seed=GongsunLi", "https://api.dicebear.com/7.x/bottts/svg?seed=Shangguan",
            "https://api.dicebear.com/7.x/bottts/svg?seed=LuBu", "https://api.dicebear.com/7.x/bottts/svg?seed=Allain",
            "https://api.dicebear.com/7.x/bottts/svg?seed=Dolia", "https://api.dicebear.com/7.x/bottts/svg?seed=Kui",
            "https://api.dicebear.com/7.x/bottts/svg?seed=Yaria"
        ]
    })
    
    # Scrim & Match History Data
    scrims = pd.DataFrame({
        "Match_ID": ["SCRIM_001", "SCRIM_002", "SCRIM_003", "SCRIM_004"],
        "Opponent": ["Team Alpha", "Nova Esports", "Talon Esports", "Team Liquid"],
        "Result": ["Win", "Loss", "Win", "Win"],
        "Our_KDA": ["18/5/32", "10/22/14", "25/12/40", "15/7/22"],
        "Gold_Diff": [4500, -6200, 8100, 3200],
        "Duration": ["14:22", "19:45", "16:10", "13:55"]
    })
    
    # Player Stats for Radar Charts
    players = pd.DataFrame({
        "Stat": ["KDA", "Gold/Min", "Kill Participation %", "Damage %", "Damage Taken %"],
        "Player_A (Jungler)": [4.5, 780, 72, 28, 18],
        "Player_B (Opponent Jungler)": [3.8, 710, 65, 24, 22]
    })
    
    return heroes, scrims, players

heroes_df, scrims_df, players_df = load_mock_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("👑 HoK Analyst Panel")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate to:", [
    "📊 Dashboard Overview", 
    "⚔️ Draft & Ban Analytics", 
    "👥 Player Comparison", 
    "📝 Scrims & Match History",
    "🤖 AI Coach Summary"
])

# --- EXPORT TO EXCEL FUNCTION ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()


# ==========================================
# PAGE 1: DASHBOARD OVERVIEW & HERO DATABASE
# ==========================================
if page == "📊 Dashboard Overview":
    st.title("🛡️ Honor of Kings Global Analytics")
    st.subheader("Hero Database & Meta Tiers")
    
    # Filters
    role_filter = st.selectbox("Filter by Role:", ["All"] + list(heroes_df["Role"].unique()))
    filtered_heroes = heroes_df if role_filter == "All" else heroes_df[heroes_df["Role"] == role_filter]
    
    # Grid Layout for Hero Portraits
    cols = st.columns(4)
    for index, row in filtered_heroes.iterrows():
        with cols[index % 4]:
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            st.image(row["Image_Url"], width=80)
            st.markdown(f"### **{row['Hero']}**")
            st.markdown(f"**Role:** {row['Role']}")
            st.markdown(f"📊 **Win Rate:** `{row['Win_Rate']}%`")
            st.markdown(f"🚫 **Ban Rate:** `{row['Ban_Rate']}%`")
            st.markdown(f'</div>', unsafe_allow_html=True)


# ==========================================
# PAGE 2: DRAFT & BAN ANALYTICS
# ==========================================
elif page == "⚔️ Draft & Ban Analytics":
    st.title("⚔️ Simulation Draft & Ban Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Top Priority Bans")
        fig_ban = px.bar(heroes_df.sort_values(by="Ban_Rate", ascending=False), 
                         x="Hero", y="Ban_Rate", color="Role", title="Global Ban Priority Rates")
        st.plotly_chart(fig_ban, use_container_width=True)
        
    with col2:
        st.subheader("💡 Strategic Counter-Pick Assistant")
        selected_enemy = st.selectbox("Select Threat Enemy Hero:", heroes_df["Hero"].unique())
        counter = heroes_df[heroes_df["Hero"] == selected_enemy]["Counter_Pick"].values[0]
        st.success(f"Recommended Counter Pick to lock down **{selected_enemy}**: 👉 **{counter}**")


# ==========================================
# PAGE 3: PLAYER COMPARISON (RADAR)
# ==========================================
elif page == "👥 Player Comparison":
    st.title("👥 Performance Analysis (Radar Matrix)")
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
          r=players_df["Player_A (Jungler)"],
          theta=players_df["Stat"],
          fill='toself',
          name='Our Jungler'
    ))
    fig.add_trace(go.Scatterpolar(
          r=players_df["Player_B (Opponent Jungler)"],
          theta=players_df["Stat"],
          fill='toself',
          name='Opponent Jungler'
    ))
    fig.update_layout(
      polar=dict(radialaxis=dict(visible=True, range=[0, 800])),
      showlegend=True,
      title="Our Jungler vs Opponent Jungler Head-to-Head"
    )
    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# PAGE 4: SCRIMS & MATCH HISTORY
# ==========================================
elif page == "📝 Scrims & Match History":
    st.title("📝 Scrimmage Logs & Match Database")
    
    # Interactive Table
    st.dataframe(scrims_df, use_container_width=True)
    
    # Export options
    st.subheader("📥 Export Data Reports")
    col1, col2 = st.columns(2)
    
    with col1:
        excel_data = to_excel(scrims_df)
        st.download_button(
            label="📥 Export Scrims to Excel",
            data=excel_data,
            file_name="HoK_Scrim_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col2:
        # Simplistic CSV/Raw string download mimicking layout for PDF alternative natively
        csv = scrims_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Export Scrims to CSV", data=csv, file_name="HoK_Scrims.csv", mime="text/csv")


# ==========================================
# PAGE 5: AI COACH SUMMARY GENERATOR
# ==========================================
elif page == "🤖 AI Coach Summary":
    st.title("🤖 AI Analyst Coach Corner")
    st.write("Processing latest scrimmage match history and draft behaviors...")
    
    # Logic to construct automated analytical summaries
    win_count = len(scrims_df[scrims_df["Result"] == "Win"])
    loss_count = len(scrims_df[scrims_df["Result"] == "Loss"])
    avg_gold_diff = scrims_df["Gold_Diff"].mean()
    
    st.info("### 📋 AI Tactical Report Summary")
    
    report = f"""
    **Current Form Summary:**
    Our team has a **{win_count}W - {loss_count}L** records out of recent scrims. 
    Average team economic differential rests at **+{avg_gold_diff} Gold** by game end.
    
    **Strategic Insights:**
    1. **Early Game Snowballing:** Wins correspond closely to keeping *Dolia* away from enemies while utilizing *Lam* or *Gongsun Li* down lane maps. 
    2. **Draft Bottleneck:** In our loss against *Nova Esports*, macro rotation suffered due to high-priority bans hitting our Mage pool (*Shangguan* locked out). 
    3. **Actionable Improvement:** Practice flex drafts around **Allain** or **Lu Bu** to disguise lane assignment intent during ban phases.
    """
    st.markdown(report)
