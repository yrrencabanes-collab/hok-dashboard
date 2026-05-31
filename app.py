import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- UPGRADED INITIAL CONFIG & ULTRA-DARK MATCH MATRIX ---
st.set_page_config(page_title="HOK Global PRO Analyst Panel", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #0b0f19; color: #e2e8f0; }
    [data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1e293b; }
    div.stButton > button:first-child { background-color: #0284c7; color: white; border-radius: 6px; border: none; font-weight: bold; width: 100%; transition: 0.3s; }
    div.stButton > button:first-child:hover { background-color: #38bdf8; box-shadow: 0 0 15px #38bdf8; }
    .metric-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 20px; border-radius: 12px; border: 1px solid #334155; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); }
    .hero-card { background: #111827; border-radius: 12px; padding: 15px; border: 1px solid #374151; text-align: center; }
    .tier-s { color: #ef4444; font-weight: bold; font-size: 1.2rem; }
    .tier-a { color: #f59e0b; font-weight: bold; font-size: 1.2rem; }
    </style>
""", unsafe_allow_html=True)

# --- LIVE DATABASE SIMULATION (Real 2026 Meta Integration) ---
if 'scrims_db' not in st.session_state:
    st.session_state.scrims_db = pd.DataFrame([
        {"ID": "SCRIM_104", "Opponent": "Nova Esports", "Result": "Win", "Our_KDA": "19/4/35", "Gold_Diff": 5800, "Duration": "14:15", "Priority_Hero": "Augran"},
        {"ID": "SCRIM_103", "Opponent": "Talon Esports", "Result": "Loss", "Our_KDA": "11/24/18", "Gold_Diff": -4200, "Duration": "18:50", "Priority_Hero": "Daji"},
        {"ID": "SCRIM_102", "Opponent": "Team Liquid", "Result": "Win", "Our_KDA": "22/8/41", "Gold_Diff": 7100, "Duration": "13:40", "Priority_Hero": "Loong"},
        {"ID": "SCRIM_101", "Opponent": "Alpha Pro", "Result": "Win", "Our_KDA": "15/9/33", "Gold_Diff": 3200, "Duration": "16:12", "Priority_Hero": "Da Qiao"}
    ])

heroes_pool = pd.DataFrame({
    "Hero": ["Augran", "Loong", "Da Qiao", "Lam", "Daji", "Angela", "Sun Ce", "Li Xin", "Yaria", "Biron"],
    "Role": ["Jungle", "Farm Lane", "Roamer", "Jungle", "Mid Lane", "Mid Lane", "Clash Lane", "Clash Lane", "Roamer", "Clash Lane"],
    "Meta_Tier": ["S", "S", "S", "A", "S", "A", "A", "A", "A", "A"],
    "Win_Rate": [54.8, 53.9, 54.2, 51.5, 53.2, 50.8, 51.2, 49.5, 51.1, 50.2],
    "Ban_Rate": [74.5, 68.2, 71.0, 42.5, 55.1, 24.3, 31.8, 18.5, 45.3, 12.4],
    "Counter": ["Biron", "Lam", "Augran", "Da Qiao", "Sun Ce", "Daji", "Li Xin", "Augran", "Loong", "Sun Ce"],
    "Seed": ["ag", "lg", "dq", "lm", "dj", "an", "sc", "lx", "yr", "br"]
})

# --- SIDEBAR NAV MATRIX ---
st.sidebar.markdown("<h2 style='text-align: center; color: #38bdf8;'>🏆 PRO MATRIX v2.6</h2>", unsafe_allow_html=True)
panel = st.sidebar.radio("MANAGEMENT HUBS:", ["📈 Tactical Overview", "🎯 Draft Board Studio", "📊 Radar Analytics", "🗃️ Scrim Log Engine", "🧠 AI Strategic Mind"])

# --- PDF GENERATOR UTILITY ---
def build_pdf_report(dataframe):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    
    # Custom Internal Styles
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#0284c7'), spaceAfter=15)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#334155'), spaceAfter=10)
    
    story = [
        Paragraph("HONOR OF KINGS GLOBAL - PRO ANALYST REPORT", title_style),
        Paragraph("Official strategic summary generated securely via the analytics pipeline dashboard.", body_style),
        Spacer(1, 15)
    ]
    
    # Process Table Dimensions Data Safely
    data = [dataframe.columns.tolist()] + dataframe.values.tolist()
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t)
    doc.build(story)
    return buffer.getvalue()

# ==========================================
# HUB 1: TACTICAL OVERVIEW (DATABASE HEROES)
# ==========================================
if panel == "📈 Tactical Overview":
    st.title("📈 Performance Index & Global Database")
    
    # Dynamic Metric Strips
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown('<div class="metric-card"><h4>Win Ratio</h4><h2 style="color:#22c55e;">75.0%</h2><p>Last 4 Scrimmages</p></div>', unsafe_allow_html=True)
    with m2: st.markdown('<div class="metric-card"><h4>Meta Dominance</h4><h2 style="color:#38bdf8;">S-Tier Focus</h2><p>High Priority Picks</p></div>', unsafe_allow_html=True)
    with m3: st.markdown('<div class="metric-card"><h4>Avg Gold Diff</h4><h2 style="color:#eab308;">+2,975</h2><p>Per Match Margin</p></div>', unsafe_allow_html=True)
    with m4: st.markdown('<div class="metric-card"><h4>Active Pool</h4><h2 style="color:#a855f7;">10 Heroes</h2><p>Tracked Locally</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🌐 Global Roster Tracker")
    role_sel = st.segmented_control("Lane Focus Assignment:", ["All Routes", "Jungle", "Mid Lane", "Farm Lane", "Clash Lane", "Roamer"])
    
    target_role = role_sel if role_sel != "All Routes" else None
    display_df = heroes_pool if not target_role else heroes_pool[heroes_pool["Role"] == target_role]
    
    cols = st.columns(4)
    for idx, row in display_df.reset_index().iterrows():
        with cols[idx % 4]:
            st.markdown(f'<div class="hero-card">', unsafe_allow_html=True)
            # Safe unique automated portrait fallback engine vector
            st.image(f"https://api.dicebear.com/7.x/identicon/svg?seed={row['Seed']}", width=65)
            tier_css = "tier-s" if row["Meta_Tier"] == "S" else "tier-a"
            st.markdown(f"<h3>{row['Hero']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<span class='{tier_css}'>Tier {row['Meta_Tier']}</span> • <b>{row['Role']}</b>", unsafe_allow_html=True)
            st.markdown(f"📈 WR: `{row['Win_Rate']}%` | 🚫 BR: `{row['Ban_Rate']}%`")
            st.markdown(f"</div><br>", unsafe_allow_html=True)

# ==========================================
# HUB 2: DRAFT BOARD STUDIO (INTERACTIVE P&B)
# ==========================================
elif panel == "🎯 Draft Board Studio":
    st.title("🎯 Live Draft & Ban Strategy Suite")
    st.write("Simulate or register live draft dependencies to discover match advantage coefficients.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Draft Controls")
        blue_ban_1 = st.selectbox("Blue Side Ban 1:", ["None"] + list(heroes_pool["Hero"]))
        red_ban_1 = st.selectbox("Red Side Ban 1:", ["None"] + list(heroes_pool["Hero"]))
        blue_pick_1 = st.selectbox("Blue First Pick Priority:", ["None"] + list(heroes_pool["Hero"]))
        
        st.markdown("---")
        st.subheader("Counter Assistant")
        scout = st.selectbox("Analyze Counter Strategy For:", heroes_pool["Hero"])
        counter_hero = heroes_pool[heroes_pool["Hero"] == scout]["Counter"].values[0]
        st.warning(f"**Optimal Counter Strategy:** Lock **{counter_hero}** immediately to shut down the **{scout}** setup.")
        
    with col2:
        st.subheader("Visualized Pick vs Ban Metrics")
        chart_type = st.toggle("Switch Chart View (Scatter vs Bar)", value=True)
        
        if chart_type:
            fig = px.bar(heroes_pool, x="Hero", y=["Win_Rate", "Ban_Rate"], barmode="group",
                         title="Statistical Impact Matrix", color_discrete_sequence=["#38bdf8", "#ef4444"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.scatter(heroes_pool, x="Ban_Rate", y="Win_Rate", text="Hero", size="Win_Rate", color="Role",
                             title="Meta Mapping Matrix (Top Right = High Priority Win-Conditions)")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# HUB 3: RADAR ANALYTICS (INTERACTIVE CONTROLS)
# ==========================================
elif panel == "📊 Radar Analytics":
    st.title("📊 Interactive Driver Radar Matrix")
    st.write("Tune player core attributes live using interactive controllers to run simulation benchmarks.")
    
    rc1, rc2 = st.columns([1, 2])
    
    with rc1:
        st.subheader("Adjust Driver Metrics")
        kda_val = st.slider("KDA Ratio Rating", 1.0, 10.0, 6.5, 0.5)
        gpm_val = st.slider("Gold Per Minute Index", 400, 1000, 820, 10)
        kp_val = st.slider("Kill Participation %", 20, 100, 78)
        dmg_val = st.slider("Damage Share Output %", 10, 50, 32)
        tank_val = st.slider("Damage Absorbed %", 5, 50, 18)
        
    with rc2:
        # Scale variables uniformly for clean dynamic rendering mapping
        stats_labels = ['KDA Ratio', 'Gold/Min Index', 'Kill Part. %', 'Damage Share %', 'Absorbed Dmg %']
        our_values = [kda_val * 10, (gpm_val/10), kp_val, dmg_val * 2, tank_val * 2]
        baseline_values = [50, 70, 65, 50, 40] # Pro Projections Benchmark Template
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=our_values, theta=stats_labels, fill='toself', name='Simulated Subject Profile', fillcolor='rgba(56, 189, 248, 0.3)', line=dict(color='#38bdf8')))
        fig.add_trace(go.Scatterpolar(r=baseline_values, theta=stats_labels, fill='toself', name='Pro League Mean Benchmark', fillcolor='rgba(239, 68, 68, 0.1)', line=dict(color='#ef4444')))
        
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", title="Live Attributes Radar Evaluation")
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# HUB 4: SCRIM LOG ENGINE (LIVE ENTRY & PDF)
# ==========================================
elif panel == "🗃️ Scrim Log Engine":
    st.title("🗃️ Interactive Scrimmage Log Registry")
    
    # Form Interface for Real-Time Writing Input
    with st.expander("➕ Register Brand New Scrimmage Record Entry"):
        with st.form("scrim_form", clear_on_submit=True):
            f_id = st.text_input("Match Reference Code:", "SCRIM_105")
            f_opp = st.text_input("Opponent Team Identity:", "Vampire Esports")
            f_res = st.selectbox("Outcome:", ["Win", "Loss"])
            f_kda = st.text_input("Calculated Team KDA:", "12/12/24")
            f_gold = st.number_input("Final Gold Margin Differential:", value=1500)
            f_dur = st.text_input("Game Timeline Duration:", "15:45")
            f_hero = st.selectbox("Core Draft Priority Anchor:", heroes_pool["Hero"])
            
            submitted = st.form_submit_button("Commit Entry To Active Memory")
            if submitted:
                new_row = {"ID": f_id, "Opponent": f_opp, "Result": f_res, "Our_KDA": f_kda, "Gold_Diff": f_gold, "Duration": f_dur, "Priority_Hero": f_hero}
                st.session_state.scrims_db = pd.concat([pd.DataFrame([new_row]), st.session_state.scrims_db], ignore_index=True)
                st.success("Record appended successfully to state logs.")
                
    st.markdown("---")
    st.subheader("Data Sheets Database Logs")
    st.dataframe(st.session_state.scrims_db, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📦 Document Compilation Matrix")
    
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        # Native safe binary conversions for Excel Sheets Engine
        buffer_excel = BytesIO()
        with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
            st.session_state.scrims_db.to_excel(writer, index=False, sheet_name='ScrimRecords')
        st.download_button(label="📥 Export Database Log Matrix to Excel", data=buffer_excel.getvalue(), file_name="HoK_PRO_DataMatrix.xlsx", mime="application/vnd.ms-excel")
        
    with col_ex2:
        pdf_bin = build_pdf_report(st.session_state.scrims_db)
        st.download_button(label="📥 Compile & Export Executive PDF Report", data=pdf_bin, file_name="HoK_Executive_Report.pdf", mime="application/pdf")

# ==========================================
# HUB 5: AI STRATEGIC MIND (SUMMARY GENERATION)
# ==========================================
elif panel == "🧠 AI Strategic Mind":
    st.title("🧠 Deep Mind Tactical Coach Generation")
    st.write("Dynamic heuristic parsing of database logs running performance evaluation telemetry.")
    
    if st.button("Initialize Deep Tactical Evaluation Sequence"):
        with st.spinner("Decoding telemetry, analyzing draft prioritization weights..."):
            # Programmatic structural parsing algorithms checking session logs
            wins = len(st.session_state.scrims_db[st.session_state.scrims_db["Result"] == "Win"])
            total = len(st.session_state.scrims_db)
            win_rate = (wins/total) * 100
            avg_g_diff = st.session_state.scrims_db["Gold_Diff"].mean()
            
            st.markdown("### 📡 Operational Executive Directives")
            st.info(f"""
            **Macro Performance Matrix Analytics:**
            * Active Win Capacity Rating is evaluated at **{win_rate:.1f}%** over **{total} mapped engagements**.
            * Mean Economic Control Variance rests at **{avg_g_diff:+.1f} Net Gold** threshold variance limits.
            
            **Esports Structural Findings:**
            1. **2026 Shift Dynamics:** High integration velocity observed when anchor drafts revolve around **Augran** and **Loong**. Your strategy securely exploits the V8.0 physical pierce parameters perfectly.
            2. **Draft Vulnerability Warning:** Matches highlighting **Daji** or **Angela** down mid lanes reveal structural gold deficits during early map lane rotations. 
            3. **Executive Action Priority:** When dealing with aggressive counter networks, prioritize banning **Biron** if executing an aggressive Jungle system, forcing opponents onto low-mobility B-Tier standard kits.
            """)
