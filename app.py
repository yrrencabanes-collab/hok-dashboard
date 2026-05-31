import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Systemic Chaos - HoK Dashboard",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MOCK DATA GENERATION ---
# Roster Data
roster = {
    "Player": ["Dex", "Naksu", "Shinvonn", "Niel", "Yzah", "Nowiii"],
    "Role": ["Roamer / Captain", "Clash Lane", "Jungler / Head Coach", "Mid Lane", "Farm Lane", "Substitute"],
    "Win Rate (%)": [68, 72, 65, 70, 74, 60],
    "KDA": [4.2, 3.8, 4.5, 4.1, 5.2, 3.5],
    "Signature Hero": ["Dolia", "Biron", "Lam", "Mai Shiranui", "Marco Polo", "Lu Bu"]
}
df_roster = pd.DataFrame(roster)

# Hero Pool Data
heroes_data = {
    "Hero": ["Dolia", "Biron", "Lam", "Mai Shiranui", "Marco Polo", "Lu Bu", "Sima Yi", "Alessio", "Lian Po", "Shangguan"],
    "Lane": ["Roam", "Clash", "Jungle", "Mid", "Farm", "Clash", "Jungle", "Farm", "Roam", "Mid"],
    "Win Rate (%)": [75, 64, 70, 68, 72, 58, 62, 65, 55, 71],
    "Pick Count": [12, 11, 15, 10, 14, 9, 8, 10, 6, 7]
}
df_heroes = pd.DataFrame(heroes_data)

# --- SIDEBAR NAV & TEAM INFO ---
st.sidebar.image("https://img.icons8.com/colors/96/chaos.png", width=80) # Placeholder cool logo
st.sidebar.title("Systemic Chaos")
st.sidebar.markdown("**Honor of Kings Analyst Suite**")
st.sidebar.divider()

# Staff Roles
st.sidebar.subheader("📋 Staff Management")
st.sidebar.markdown("**Head Coach:** Shinvonn")
st.sidebar.markdown("**Analyst Coach / Capt:** Dex")
st.sidebar.divider()

# Navigation
menu = st.sidebar.radio("Navigate Dashboard", ["Overview & Roster", "Hero Analytics", "Draft Simulator", "Coaches' Strategic Notes"])

# --- SCREEN 1: OVERVIEW & ROSTER ---
if menu == "Overview & Roster":
    st.title("⚔️ Systemic Chaos - Team Performance Overview")
    st.markdown("Welcome to the analytical core of Systemic Chaos. Track rosters, individual KPIs, and core match metrics below.")
    
    # Top Level Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Scrims/Matches", value="58", delta="+5 this week")
    with col2:
        st.metric(label="Overall Win Rate", value="68.4%", delta="2.1%")
    with col3:
        st.metric(label="Average Team KDA", value="4.22")
    with col4:
        st.metric(label="Current Win Streak", value="4 Wins")
        
    st.divider()
    
    # Active Roster Breakdown
    st.subheader("👥 Active Roster & Live KPI Tracking")
    
    # Highlight the Captain and Coach
    def highlight_roles(val):
        if 'Captain' in val:
            return 'background-color: rgba(255, 215, 0, 0.2); font-weight: bold;'
        elif 'Head Coach' in val:
            return 'background-color: rgba(30, 144, 255, 0.2); font-weight: bold;'
        return ''
    
    styled_df = df_roster.style.applymap(highlight_roles, subset=['Role'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Visualizing Player KDA vs Win Rate
    st.subheader("📊 Player Performance Matrix")
    fig = px.scatter(
        df_roster, 
        x="KDA", 
        y="Win Rate (%)", 
        text="Player", 
        color="Role", 
        size="Win Rate (%)",
        title="Player Impact Map (Size = Win Rate)"
    )
    fig.update_traces(textposition='top center')
    st.plotly_chart(fig, use_container_width=True)

# --- SCREEN 2: HERO ANALYTICS ---
elif menu == "Hero Analytics":
    st.title("📈 Hero Pool & Meta Analysis")
    st.markdown("Analyze the comfort picks and meta priorities for Systemic Chaos execution.")
    
    # Filter by lane
    lanes = ["All"] + list(df_heroes["Lane"].unique())
    selected_lane = st.selectbox("Filter by Map Lane:", lanes)
    
    filtered_heroes = df_heroes if selected_lane == "All" else df_heroes[df_heroes["Lane"] == selected_lane]
    
    # Charts Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Most Contended Heroes (Picks)")
        fig_bar = px.bar(
            filtered_heroes.sort_values(by="Pick Count", ascending=False),
            x="Hero",
            y="Pick Count",
            color="Lane",
            text_auto=True,
            theme="plotly_dark"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.subheader("Win Rates per Hero")
        fig_pie = px.pie(
            filtered_heroes,
            values="Win Rate (%)",
            names="Hero",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# --- SCREEN 3: DRAFT SIMULATOR ---
elif menu == "Draft Simulator":
    st.title("🧠 Draft Strategy & Counter-Pick Simulator")
    st.markdown("Simulate a Ban/Pick phase against opponents to lock in synergy priorities.")
    
    all_hok_heroes = ["Dolia", "Biron", "Lam", "Mai Shiranui", "Marco Polo", "Lu Bu", "Sima Yi", "Alessio", "Lian Po", "Shangguan", "Gao", "Guan Yu", "Heino", "Allain"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔵 Systemic Chaos (Blue Side)")
        blue_ban1 = st.selectbox("Ban 1", ["None"] + all_hok_heroes, key="bb1")
        blue_ban2 = st.selectbox("Ban 2", ["None"] + all_hok_heroes, key="bb2")
        
        st.markdown("**Picks:**")
        p1 = st.selectbox("Clash Lane Pick (Naksu)", all_hok_heroes, index=1)
        p2 = st.selectbox("Jungler Pick (Shinvonn)", all_hok_heroes, index=2)
        p3 = st.selectbox("Mid Lane Pick (Niel)", all_hok_heroes, index=3)
        p4 = st.selectbox("Farm Lane Pick (Yzah)", all_hok_heroes, index=4)
        p5 = st.selectbox("Roamer Pick (Dex)", all_hok_heroes, index=0)
        
    with col2:
        st.subheader("🔴 Enemy Team (Red Side)")
        red_ban1 = st.selectbox("Ban 1", ["None"] + all_hok_heroes, key="rb1")
        red_ban2 = st.selectbox("Ban 2", ["None"] + all_hok_heroes, key="rb2")
        
        st.markdown("**Picks:**")
        ep1 = st.selectbox("Enemy Clash", all_hok_heroes, index=5)
        ep2 = st.selectbox("Enemy Jungle", all_hok_heroes, index=6)
        ep3 = st.selectbox("Enemy Mid", all_hok_heroes, index=10)
        ep4 = st.selectbox("Enemy Farm", all_hok_heroes, index=7)
        ep5 = st.selectbox("Enemy Roam", all_hok_heroes, index=8)

    st.divider()
    st.subheader("📋 Analyst Breakdown Matrix")
    
    # Simple simulated logic for synergy check
    if p1 == "Biron" and p5 == "Dolia":
        st.success("🔥 **Synergy Detected:** Biron + Dolia allows double ultimate execution! Highly favorable dive comp.")
    elif p3 == "Mai Shiranui" and p2 == "Lam":
        st.info("⚡ **Burst Comp Active:** High burst damage composition. Focus early game skirmishes around the Abyssal Dragon.")
    else:
        st.warning("⚖️ **Standard Composition:** Balanced scaling. Standard visual checks pass. Watch out for enemy poke variants.")

# --- SCREEN 4: COACHES' STRATEGIC NOTES ---
elif menu == "Coaches' Strategic Notes":
    st.title("📝 Strategy Room & Notes")
    st.markdown("Direct tactical directives from **Head Coach Shinvonn** and **Analyst Coach Dex**.")
    
    # Coach Feedbacks
    with st.expander("📌 Shinvonn's Head Coach Directives", expanded=True):
        st.markdown("""
        1. **Objective Priority:** We are giving up too much control over the first Tempest Dragon. Early rotations from **Niel (Mid)** and **Dex (Roam)** must secure river priority by minute 9:30.
        2. **Naksu (Clash):** Keep practicing the flank timing with Biron when teleportation portals open up.
        3. **Nowiii (Sub):** Be ready to sub in for Game 3 on our pocket triple-flex strategies.
        """)
        
    with st.expander("📊 Dex's Analyst Breakdown", expanded=False):
        st.markdown("""
        * **Meta Shift:** Version update buffed magical defense items. **Niel**, try prioritizing flat magic penetration early instead of raw scaling power.
        * **Yzah (Farm):** Your positioning with Marco Polo in teamfights yielded a 74% win rate when utilizing the Dolia cooldown refresh. Keep running this combo during scrims.
        """)
        
    # Interactive Note Submitter
    st.subheader("📥 Submit New Strategic Note")
    author = st.selectbox("Author", ["Shinvonn (Head Coach)", "Dex (Analyst Coach/Capt)"])
    new_note = st.text_area("Write directive here...")
    
    if st.button("Publish Directive"):
        if new_note:
            st.toast(f"New note by {author} saved successfully!", icon="💾")
            # In a real app, you would append this to a database or a tracking CSV file.
            st.info(f"**Latest Entry ({author}):** {new_note}")
        else:
            st.error("Cannot publish an empty note!")
