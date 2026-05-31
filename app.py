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
    
    /* Tier Colors & Style Designations */
    .tier-s-header { background: linear-gradient(90deg, #ef4444 0%, #7f1d1d 100%); color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 1.3rem; margin-top: 20px; border-left: 5px solid #ff3b30; }
    .tier-a-header { background: linear-gradient(90deg, #f59e0b 0%, #78350f 100%); color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 1.3rem; margin-top: 20px; border-left: 5px solid #ffcc00; }
    .tier-b-header { background: linear-gradient(90deg, #3b82f6 0%, #1e3a8a 100%); color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 1.3rem; margin-top: 20px; border-left: 5px solid #007aff; }
    .tier-c-header { background: linear-gradient(90deg, #10b981 0%, #064e3b 100%); color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 1.3rem; margin-top: 20px; border-left: 5px solid #34c759; }
    .tier-d-header { background: linear-gradient(90deg, #6b7280 0%, #374151 100%); color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 1.3rem; margin-top: 20px; border-left: 5px solid #8e8e93; }
    
    .tier-s { color: #ef4444; font-weight: bold; font-size: 1.15rem; }
    .tier-a { color: #f59e0b; font-weight: bold; font-size: 1.15rem; }
    .tier-b { color: #3b82f6; font-weight: bold; font-size: 1.15rem; }
    .tier-c { color: #10b981; font-weight: bold; font-size: 1.15rem; }
    .tier-d { color: #9ca3af; font-weight: bold; font-size: 1.15rem; }
    </style>
""", unsafe_allow_html=True)

# --- LIVE DATABASE SIMULATION ---
if 'scrims_db' not in st.session_state:
    st.session_state.scrims_db = pd.DataFrame([
        {"ID": "SCRIM_104", "Opponent": "Nova Esports", "Result": "Win", "Our_KDA": "19/4/35", "Gold_Diff": 5800, "Duration": "14:15", "Priority_Hero": "Augran"},
        {"ID": "SCRIM_103", "Opponent": "Talon Esports", "Result": "Loss", "Our_KDA": "11/24/18", "Gold_Diff": -4200, "Duration": "18:50", "Priority_Hero": "Daji"},
        {"ID": "SCRIM_102", "Opponent": "Team Liquid", "Result": "Win", "Our_KDA": "22/8/41", "Gold_Diff": 7100, "Duration": "13:40", "Priority_Hero": "Loong"},
        {"ID": "SCRIM_101", "Opponent": "Alpha Pro", "Result": "Win", "Our_KDA": "15/9/33", "Gold_Diff": 3200, "Duration": "16:12", "Priority_Hero": "Da Qiao"}
    ])

# Expanded 2026 Comprehensive Hero Meta Tier Database
heroes_pool = pd.DataFrame([
    # S Tier
    {"Hero": "Augran", "Role": "Jungle", "Meta_Tier": "S", "Win_Rate": 54.8, "Ban_Rate": 74.5, "Counter": "Biron", "Seed": "ag"},
    {"Hero": "Loong", "Role": "Farm Lane", "Meta_Tier": "S", "Win_Rate": 53.9, "Ban_Rate": 68.2, "Counter": "Lam", "Seed": "lg"},
    {"Hero": "Da Qiao", "Role": "Roamer", "Meta_Tier": "S", "Win_Rate": 54.2, "Ban_Rate": 71.0, "Counter": "Augran", "Seed": "dq"},
    {"Hero": "Daji", "Role": "Mid Lane", "Meta_Tier": "S", "Win_Rate": 53.2, "Ban_Rate": 55.1, "Counter": "Sun Ce", "Seed": "dj"},
    {"Hero": "Lam", "Role": "Jungle", "Meta_Tier": "S", "Win_Rate": 52.8, "Ban_Rate": 62.4, "Counter": "Dolia", "Seed": "lm"},
    {"Hero": "Sun Ce", "Role": "Clash Lane", "Meta_Tier": "S", "Win_Rate": 53.1, "Ban_Rate": 48.0, "Counter": "Li Xin", "Seed": "sc"},
    {"Hero": "Li Xin", "Role": "Clash Lane", "Meta_Tier": "S", "Win_Rate": 52.9, "Ban_Rate": 46.5, "Counter": "Biron", "Seed": "lx"},
    {"Hero": "Arke", "Role": "Jungle", "Meta_Tier": "S", "Win_Rate": 52.7, "Ban_Rate": 50.2, "Counter": "Da Qiao", "Seed": "ak"},
    {"Hero": "Yaria", "Role": "Roamer", "Meta_Tier": "S", "Win_Rate": 52.6, "Ban_Rate": 49.8, "Counter": "Loong", "Seed": "yr"},

    # A Tier
    {"Hero": "Angela", "Role": "Mid Lane", "Meta_Tier": "A", "Win_Rate": 51.5, "Ban_Rate": 24.3, "Counter": "Daji", "Seed": "an"},
    {"Hero": "Biron", "Role": "Clash Lane", "Meta_Tier": "A", "Win_Rate": 50.8, "Ban_Rate": 12.4, "Counter": "Sun Ce", "Seed": "br"},
    {"Hero": "Garo", "Role": "Farm Lane", "Meta_Tier": "A", "Win_Rate": 51.2, "Ban_Rate": 30.5, "Counter": "Lam", "Seed": "gr"},
    {"Hero": "Dolia", "Role": "Roamer", "Meta_Tier": "A", "Win_Rate": 51.9, "Ban_Rate": 45.2, "Counter": "Augran", "Seed": "dl"},
    {"Hero": "Arthur", "Role": "Clash Lane", "Meta_Tier": "A", "Win_Rate": 51.1, "Ban_Rate": 15.0, "Counter": "Li Xin", "Seed": "rt"},
    {"Hero": "Wukong", "Role": "Jungle", "Meta_Tier": "A", "Win_Rate": 50.9, "Ban_Rate": 35.4, "Counter": "Dian Wei", "Seed": "wk"},
    {"Hero": "Yixing", "Role": "Mid Lane", "Meta_Tier": "A", "Win_Rate": 50.4, "Ban_Rate": 18.2, "Counter": "Yaria", "Seed": "yx"},

    # B Tier
    {"Hero": "Dian Wei", "Role": "Jungle", "Meta_Tier": "B", "Win_Rate": 49.8, "Ban_Rate": 12.1, "Counter": "Lam", "Seed": "dw"},
    {"Hero": "Milady", "Role": "Mid Lane", "Meta_Tier": "B", "Win_Rate": 49.5, "Ban_Rate": 14.5, "Counter": "Angela", "Seed": "ml"},
    {"Hero": "Lady Sun", "Role": "Farm Lane", "Meta_Tier": "B", "Win_Rate": 49.6, "Ban_Rate": 22.1, "Counter": "Garo", "Seed": "ls"},
    {"Hero": "Cai Yan", "Role": "Roamer", "Meta_Tier": "B", "Win_Rate": 49.1, "Ban_Rate": 10.8, "Counter": "Da Qiao", "Seed": "cy"},
    {"Hero": "Lu Bu", "Role": "Clash Lane", "Meta_Tier": "B", "Win_Rate": 48.9, "Ban_Rate": 8.5, "Counter": "Biron", "Seed": "lb"},
    {"Hero": "Li Bai", "Role": "Jungle", "Meta_Tier": "B", "Win_Rate": 48.5, "Ban_Rate": 11.2, "Counter": "Arke", "Seed": "lb_j"},

    # C Tier
    {"Hero": "Diaochan", "Role": "Mid Lane", "Meta_Tier": "C", "Win_Rate": 47.5, "Ban_Rate": 8.0, "Counter": "Daji", "Seed": "dc"},
    {"Hero": "Han Xin", "Role": "Jungle", "Meta_Tier": "C", "Win_Rate": 47.1, "Ban_Rate": 9.4, "Counter": "Wukong", "Seed": "hx"},
    {"Hero": "Di Renjie", "Role": "Farm Lane", "Meta_Tier": "C", "Win_Rate": 47.8, "Ban_Rate": 5.2, "Counter": "Loong", "Seed": "dr"},
    {"Hero": "Zilong", "Role": "Jungle", "Meta_Tier": "C", "Win_Rate": 47.2, "Ban_Rate": 6.1, "Counter": "Augran", "Seed": "zl"},
    {"Hero": "Sakeer", "Role": "Roamer", "Meta_Tier": "C", "Win_Rate": 46.5, "Ban_Rate": 2.5, "Counter": "Da Qiao", "Seed": "sk"},

    # D Tier
    {"Hero": "Agudo", "Role": "Jungle", "Meta_Tier": "D", "Win_Rate": 45.1, "Ban_Rate": 1.2, "Counter": "Lam", "Seed": "ag_d"},
    {"Hero": "Heino", "Role": "Mid Lane", "Meta_Tier": "D", "Win_Rate": 44.8, "Ban_Rate": 2.1, "Counter": "Angela", "Seed": "hn"},
    {"Hero": "Huang Zhong", "Role": "Farm Lane", "Meta_Tier": "D", "Win_Rate": 45.4, "Ban_Rate": 1.5, "Counter": "Garo", "Seed": "hz"},
    {"Hero": "Mulan", "Role": "Clash Lane", "Meta_Tier": "D", "Win_Rate": 44.9, "Ban_Rate": 3.0, "Counter": "Arthur", "Seed": "ml_c"}
])

# --- SIDEBAR NAV MATRIX ---
st.sidebar.markdown("<h2 style='text-align: center; color: #38bdf8;'>🏆 PRO MATRIX v2.6</h2>", unsafe_allow_html=True)
panel = st.sidebar.radio("MANAGEMENT HUBS:", [
    "📈 Tactical Overview", 
    "🏆 Meta Heroes", 
    "🎯 Draft Board Studio", 
    "📊 Radar Analytics", 
    "🗃️ Scrim Log Engine", 
    "🧠 AI Strategic Mind"
])

# --- PDF GENERATOR UTILITY ---
def build_pdf_report(dataframe):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0284c7'), spaceAfter=15)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#334155'), spaceAfter=10)
    
    story = [
        Paragraph("HONOR OF KINGS GLOBAL - PRO ANALYST REPORT", title_style),
        Paragraph("Official strategic summary generated securely via the analytics pipeline dashboard.", body_style),
        Spacer(1, 15)
    ]
    
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
# HUB 1: TACTICAL OVERVIEW
# ==========================================
if panel == "📈 Tactical Overview":
    st.title("📈 Performance Index & Tactical Insights")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown('<div class="metric-card"><h4>Win Ratio</h4><h2 style="color:#22c55e;">75.0%</h2><p>Last 4 Scrimmages</p></div>', unsafe_allow_html=True)
    with m2: st.markdown('<div class="metric-card"><h4>Meta Dominance</h4><h2 style="color:#38bdf8;">S-Tier Focus</h2><p>High Priority Picks</p></div>', unsafe_allow_html=True)
    with m3: st.markdown('<div class="metric-card"><h4>Avg Gold Diff</h4><h2 style="color:#eab308;">+2,975</h2><p>Per Match Margin</p></div>', unsafe_allow_html=True)
    with m4: st.markdown('<div class="metric-card"><h4>Active Pool</h4><h2 style="color:#a855f7;">31 Heroes</h2><p>Upgraded Meta Pool</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🌐 Mini Database Overview")
    
    role_options = ["All Routes", "Jungle", "Mid Lane", "Farm Lane", "Clash Lane", "Roamer"]
    role_sel = st.selectbox("Select Lane Focus Assignment:", role_options)
    
    target_role = role_sel if role_sel != "All Routes" else None
    display_df = heroes_pool if not target_role else heroes_pool[heroes_pool["Role"] == target_role]
    
    cols = st.columns(4)
    for idx, row in display_df.head(8).reset_index().iterrows():
        with cols[idx % 4]:
            st.markdown(f'<div class="hero-card">', unsafe_allow_html=True)
            st.image(f"https://api.dicebear.com/7.x/identicon/svg?seed={row['Seed']}", width=65)
            tier_css = f"tier-{row['Meta_Tier'].lower()}"
            st.markdown(f"<h3>{row['Hero']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<span class='{tier_css}'>Tier {row['Meta_Tier']}</span> • <b>{row['Role']}</b>", unsafe_allow_html=True)
            st.markdown(f"📈 WR: `{row['Win_Rate']}%` | 🚫 BR: `{row['Ban_Rate']}%`")
            st.markdown(f"</div><br>", unsafe_allow_html=True)

# ==========================================
# HUB 2: META HEROES TIER LIST (NEW!)
# ==========================================
elif panel == "🏆 Meta Heroes":
    st.title("🏆 Automated Meta Heroes Tier List")
    st.write("Real-time global match analysis aggregated dynamically into Honor of Kings strategic tiers (S to D).")
    
    # Filter Controls
    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        lane_filter = st.selectbox("Lane Filter:", ["All Lanes", "Jungle", "Mid Lane", "Farm Lane", "Clash Lane", "Roamer"])
    with f_col2:
        search_query = st.text_input("🔍 Quick Search Hero Name:", "").strip().lower()
        
    st.markdown("---")
    
    # Process Tier Filtering Logic
    filtered_list = heroes_pool.copy()
    if lane_filter != "All Lanes":
        filtered_list = filtered_list[filtered_list["Role"] == lane_filter]
    if search_query:
        filtered_list = filtered_list[filtered_list["Hero"].str.lower().str.contains(search_query)]
        
    tiers = ["S", "A", "B", "C", "D"]
    tier_meta_labels = {
        "S": "👑 Tier S — Meta-Defining (First Pick / Ban Priority)",
        "A": "⭐ Tier A — Strong & Reliable (Consistent Match Staples)",
        "B": "⚡ Tier B — Situational (Niche Matchup / Counter Options)",
        "C": "🛡️ Tier C — Weak / Outdated (Sub-Optimal, Map Dependent)",
        "D": "📉 Tier D — Avoid / Low Performance (Needs Direct Buffs)"
    }
    
    for t in tiers:
        tier_heroes = filtered_list[filtered_list["Meta_Tier"] == t]
        
        # Display Header Only If Heroes Exist in Category
        if not tier_heroes.empty:
            st.markdown(f'<div class="tier-{t.lower()}-header">{tier_meta_labels[t]}</div><br>', unsafe_allow_html=True)
            
            # Grid system
            t_cols = st.columns(4)
            for idx, row in tier_heroes.reset_index().iterrows():
                with t_cols[idx % 4]:
                    st.markdown(f'<div class="hero-card">', unsafe_allow_html=True)
                    st.image(f"https://api.dicebear.com/7.x/identicon/svg?seed={row['Seed']}", width=65)
                    st.markdown(f"<h3>{row['Hero']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<b>Lane:</b> {row['Role']}", unsafe_allow_html=True)
                    st.markdown(f"🔥 WR: `{row['Win_Rate']}%` | 🚫 BR: `{row['Ban_Rate']}%`")
                    st.markdown(f"🎯 <b>Optimal Counter:</b> {row['Counter']}", unsafe_allow_html=True)
                    st.markdown(f"</div><br>", unsafe_allow_html=True)
        elif search_query:
            # Skip empty sections if filtering down specific searches
            pass

# ==========================================
# HUB 3: DRAFT BOARD STUDIO
# ==========================================
elif panel == "🎯 Draft Board Studio":
    st.title("🎯 Live Draft & Ban Strategy Suite")
    
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
        chart_type = st.checkbox("Toggle Chart View (Checked = Bar, Unchecked = Scatter)", value=True)
        
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
# HUB 4: RADAR ANALYTICS
# ==========================================
elif panel == "📊 Radar Analytics":
    st.title("📊 Interactive Driver Radar Matrix")
    
    rc1, rc2 = st.columns([1, 2])
    
    with rc1:
        st.subheader("Adjust Driver Metrics")
        kda_val = st.slider("KDA Ratio Rating", 1.0, 10.0, 6.5, 0.5)
        gpm_val = st.slider("Gold Per Minute Index", 400, 1000, 820, 10)
        kp_val = st.slider("Kill Participation %", 20, 100, 78)
        dmg_val = st.slider("Damage Share Output %", 10, 50, 32)
        tank_val = st.slider("Damage Absorbed %", 5, 50, 18)
        
    with rc2:
        stats_labels = ['KDA Ratio', 'Gold/Min Index', 'Kill Part. %', 'Damage Share %', 'Absorbed Dmg %']
        our_values = [kda_val * 10, (gpm_val/10), kp_val, dmg_val * 2, tank_val * 2]
        baseline_values = [50, 70, 65, 50, 40] 
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=our_values, theta=stats_labels, fill='toself', name='Simulated Subject Profile', fillcolor='rgba(56, 189, 248, 0.3)', line=dict(color='#38bdf8')))
        fig.add_trace(go.Scatterpolar(r=baseline_values, theta=stats_labels, fill='toself', name='Pro League Mean Benchmark', fillcolor='rgba(239, 68, 68, 0.1)', line=dict(color='#ef4444')))
        
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", title="Live Attributes Radar Evaluation")
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# HUB 5: SCRIM LOG ENGINE
# ==========================================
elif panel == "🗃️ Scrim Log Engine":
    st.title("🗃️ Interactive Scrimmage Log Registry")
    
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
        buffer_excel = BytesIO()
        with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
            st.session_state.scrims_db.to_excel(writer, index=False, sheet_name='ScrimRecords')
        st.download_button(label="📥 Export Database Log Matrix to Excel", data=buffer_excel.getvalue(), file_name="HoK_PRO_DataMatrix.xlsx", mime="application/vnd.ms-excel")
        
    with col_ex2:
        pdf_bin = build_pdf_report(st.session_state.scrims_db)
        st.download_button(label="📥 Compile & Export Executive PDF Report", data=pdf_bin, file_name="HoK_Executive_Report.pdf", mime="application/pdf")

# ==========================================
# HUB 6: AI STRATEGIC MIND
# ==========================================
elif panel == "🧠 AI Strategic Mind":
    st.title("🧠 Deep Mind Tactical Coach Generation")
    
    if st.button("Initialize Deep Tactical Evaluation Sequence"):
        with st.spinner("Decoding telemetry, analyzing draft prioritization weights..."):
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
            1. **2026 Shift Dynamics:** High integration velocity observed when anchor drafts revolve around **Augran** and **Loong**. Your strategy securely exploits physical pierce parameters perfectly.
            2. **Draft Vulnerability Warning:** Matches highlighting **Daji** or **Angela** down mid lanes reveal structural gold deficits during early map lane rotations. 
            3. **Executive Action Priority:** When dealing with aggressive counter networks, prioritize banning **Biron** if executing an aggressive Jungle system, forcing opponents onto low-mobility B-Tier standard kits.
            """)

---

### 📝 Step-by-Step Guide to Deploy the Upgrade

<Sequence>
  <Step subtitle="Est. time: 1 min" title="Update GitHub Repository">
    Go to your GitHub repository and open `app.py`. Click the edit pencil icon, delete your old code entirely, paste this new script inside, and commit the changes to your `main` branch.
  </Step>
  <Step subtitle="Est. time: 1 min" title="Automatic Rebuild">
    Streamlit Community Cloud automatically detects any code changes pushed to GitHub. Go to your dashboard and wait for it to process the new updates (it will show a small "Baking" icon for a few moments).
  </Step>
  <Step subtitle="Est. time: 1 min" title="Explore 'Meta Heroes'">
    Open your live web application link. Click on the new **"🏆 Meta Heroes"** navigation option on the left sidebar to access your fully interactive, filtered tier list system!
  </Step>
</Sequence>
