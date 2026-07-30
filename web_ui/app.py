# import os
# import time
# import pandas as pd
# import streamlit as st
# import plotly.express as px
# from pathlib import Path
# import random

# # --- CONFIG ---
# st.set_page_config(page_title="CF-FUZZ NEON", layout="wide", initial_sidebar_state="expanded")

# # --- CYBERPUNK CSS ---
# st.markdown("""
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;700&display=swap');

#         /* Global Theme */
#         .stApp {
#             background: #050505;
#             color: #e2e8f0;
#             font-family: 'Space Grotesk', sans-serif !important;
#         }

#         /* Hide Streamlit Header/Footer */
#         #MainMenu, footer, header {visibility: hidden;}

#         /* Sidebar Styling */
#         [data-testid="stSidebar"] {
#             background-color: #0a0a0a !important;
#             border-right: 1px solid #1e293b;
#         }

#         /* Glassmorphism Cards */
#         .cyber-card {
#             background: rgba(15, 23, 42, 0.6);
#             backdrop-filter: blur(12px);
#             border: 1px solid rgba(56, 189, 248, 0.2);
#             border-radius: 20px;
#             padding: 25px;
#             box-shadow: 0 0 20px rgba(0,0,0,0.5);
#             margin-bottom: 20px;
#             transition: all 0.3s ease;
#         }
#         .cyber-card:hover {
#             border: 1px solid rgba(56, 189, 248, 0.5);
#             box-shadow: 0 0 30px rgba(56, 189, 248, 0.1);
#         }

#         /* Big Neon Metrics */
#         .neon-label {
#             color: #94a3b8;
#             font-size: 14px;
#             font-weight: 700;
#             letter-spacing: 2px;
#             text-transform: uppercase;
#         }
#         .neon-value {
#             font-size: 64px;
#             font-weight: 800;
#             background: linear-gradient(to bottom right, #38bdf8, #818cf8);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#             line-height: 1;
#             margin: 10px 0;
#             filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.3));
#         }

#         /* Target Display */
#         .target-pill {
#             background: rgba(56, 189, 248, 0.1);
#             color: #38bdf8;
#             padding: 4px 12px;
#             border-radius: 8px;
#             border: 1px solid rgba(56, 189, 248, 0.3);
#             font-family: 'JetBrains Mono';
#             font-size: 14px;
#         }

#         /* Scrollbar Fix */
#         ::-webkit-scrollbar { width: 8px; }
#         ::-webkit-scrollbar-track { background: #050505; }
#         ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
        
#         /* Selection Color */
#         ::selection { background: #38bdf8; color: #000; }
#     </style>
# """, unsafe_allow_html=True)

# # --- ENGINE ---
# def get_latest_telemetry(filename):
#     path = Path("cf_fuzz_output")
#     if not path.exists(): return pd.DataFrame()
#     stem = Path(filename).stem
#     files = list(path.glob(f"telemetry_{stem}_*.csv"))
#     if not files: return pd.DataFrame()
#     return pd.read_csv(max(files, key=os.path.getmtime))

# def render_code_panel(code, filename):
#     lines = code.split('\n')
#     html = f"""
#     <div style="background: #0a0a0a; border-radius: 16px; border: 1px solid #1e293b; overflow: hidden; height: 600px; display: flex; flex-direction: column;">
#         <div style="background: #111; padding: 12px 20px; border-bottom: 1px solid #1e293b; display: flex; justify-content: space-between; align-items: center;">
#             <div style="display:flex; gap:8px;">
#                 <div style="width:12px; height:12px; border-radius:50%; background:#ff5f56"></div>
#                 <div style="width:12px; height:12px; border-radius:50%; background:#ffbd2e"></div>
#                 <div style="width:12px; height:12px; border-radius:50%; background:#27c93f"></div>
#             </div>
#             <span style="color:#64748b; font-family:'JetBrains Mono'; font-size:12px;">{filename}</span>
#         </div>
#         <div style="overflow-y: auto; flex: 1; padding: 15px 0; font-family: 'JetBrains Mono'; font-size: 13px; line-height: 1.5;">
#     """
#     for i, line in enumerate(lines):
#         safe = line.replace('<', '&lt;').replace('>', '&gt;')
#         html += f"""<div style="display:flex; padding: 0 20px;">
#             <div style="width:40px; color:#334155; user-select:none; border-right:1px solid #1e293b; margin-right:15px;">{i+1}</div>
#             <div style="color:#94a3b8; white-space:pre;">{safe}</div>
#         </div>"""
#     return html + "</div></div>"

# # --- SIDEBAR ---
# with st.sidebar:
#     st.markdown("<h1 style='color:#38bdf8; font-size:28px; font-weight:800; letter-spacing:-1px;'>CF-FUZZ <span style='color:#e2e8f0'>V2</span></h1>", unsafe_allow_html=True)
#     st.markdown("<p style='color:#64748b; margin-top:-15px;'>Autonomous Stress Tester</p>", unsafe_allow_html=True)
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Locate files
#     cpp_files = list(Path("dataset").glob("*.cpp")) + list(Path("dataset_success").glob("*.cpp"))
    
#     if not cpp_files:
#         st.error("No .cpp files found in dataset/")
#         st.stop()
        
#     targets = {f.name: f for f in cpp_files}
#     selected_name = st.selectbox("Target Core", list(targets.keys()))
    
#     st.markdown("---")
#     live = st.toggle("Active Telemetry Pulse", value=True)
#     if live: time.sleep(1.5); st.rerun()

# # --- MAIN DASHBOARD ---
# target_path = targets[selected_name]
# code_text = target_path.read_text()
# df = get_latest_telemetry(target_path.name)

# # Header Stats
# peak = df['Island_Alpha_Peak_MS'].max() if not df.empty else 0.0
# gen = df['Generation'].max() if not df.empty else 0

# # 1. TOP ROW STATS
# c1, c2, c3 = st.columns([1, 1, 1.5])

# with c1:
#     st.markdown(f"""<div class="cyber-card">
#         <div class="neon-label">Peak Impact</div>
#         <div class="neon-value">{peak:.1f}<span style="font-size:24px; color:#64748b">ms</span></div>
#     </div>""", unsafe_allow_html=True)

# with c2:
#     st.markdown(f"""<div class="cyber-card">
#         <div class="neon-label">Evolution Era</div>
#         <div class="neon-value">{gen}<span style="font-size:24px; color:#64748b">/30</span></div>
#     </div>""", unsafe_allow_html=True)

# with c3:
#     status_text = "SYSTEM DEGRADING" if peak > 1500 else "OPTIMIZING ATTACK"
#     status_color = "#ef4444" if peak > 1500 else "#38bdf8"
#     st.markdown(f"""<div class="cyber-card">
#         <div class="neon-label">Engine Status</div>
#         <div style="font-size: 32px; font-weight: 800; color: {status_color}; margin-top:10px;">
#             ● {status_text}
#         </div>
#         <div style="margin-top:10px;"><span class="target-pill">PATH: {target_path.name}</span></div>
#     </div>""", unsafe_allow_html=True)

# # 2. ANALYSIS ROW
# col_graph, col_code = st.columns([1.3, 1], gap="large")

# with col_graph:
#     st.markdown("<h3 style='color:#e2e8f0; font-weight:700; margin-bottom:20px;'>Degradation Trajectory</h3>", unsafe_allow_html=True)
    
#     if not df.empty:
#         df_melt = df.melt(id_vars=['Generation'], value_vars=['Island_Alpha_Peak_MS', 'Island_Beta_Peak_MS', 'Island_Gamma_Peak_MS'], var_name='Island', value_name='ms')
#         df_melt['Island'] = df_melt['Island'].str.replace('Island_', '').str.replace('_Peak_MS', '')
        
#         fig = px.line(df_melt, x="Generation", y="ms", color="Island",
#                       color_discrete_map={"Alpha": "#38bdf8", "Beta": "#818cf8", "Gamma": "#c084fc"})
        
#         fig.update_traces(line_shape='spline', line_width=4, hovertemplate="Gen %{x}<br>%{y}ms")
#         fig.update_layout(
#             paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
#             height=500, margin=dict(l=0,r=0,t=0,b=0),
#             xaxis=dict(showgrid=True, gridcolor="#1e293b", color="#94a3b8", title="Generations"),
#             yaxis=dict(showgrid=True, gridcolor="#1e293b", color="#94a3b8", title="Latency (ms)"),
#             legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, font=dict(color="#e2e8f0"))
#         )
#         fig.add_hline(y=2000, line_dash="dash", line_color="#ef4444", annotation_text="TLE LIMIT", annotation_font_color="#ef4444")
#         st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
#     else:
#         st.info("Awaiting telemetry data stream...")

# with col_code:
#     st.markdown("<h3 style='color:#e2e8f0; font-weight:700; margin-bottom:20px;'>Neural Inspector</h3>", unsafe_allow_html=True)
#     st.markdown(render_code_panel(code_text, target_path.name), unsafe_allow_html=True)
    
    
    
    
    
    
    


# import os
# import time
# import pandas as pd
# import streamlit as st
# import plotly.express as px
# from pathlib import Path

# # --- PAGE CONFIGURATION ---
# st.set_page_config(page_title="CF-Fuzz Ultra", layout="wide", initial_sidebar_state="expanded")

# # --- THE "AMAZING" CSS INJECTION ---
# st.markdown("""
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=JetBrains+Mono:wght@500&display=swap');

#         /* Global Reset */
#         .stApp {
#             background: radial-gradient(circle at top right, #f8fafc, #eff6ff);
#             font-family: 'Plus Jakarta Sans', sans-serif !important;
#         }

#         /* Hide Streamlit Clutter */
#         #MainMenu, footer, header {visibility: hidden;}

#         /* Sidebar Styling */
#         [data-testid="stSidebar"] {
#             background-color: rgba(255, 255, 255, 0.8) !important;
#             backdrop-filter: blur(10px);
#             border-right: 1px solid #e2e8f0;
#         }

#         /* Custom Status Card */
#         .status-card {
#             background: white;
#             padding: 2rem;
#             border-radius: 24px;
#             border: 1px solid #e2e8f0;
#             box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
#             margin-bottom: 2rem;
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#         }

#         .metric-title {
#             color: #64748b;
#             text-transform: uppercase;
#             letter-spacing: 0.1em;
#             font-size: 12px;
#             font-weight: 800;
#             margin-bottom: 8px;
#         }

#         .metric-value-huge {
#             color: #0f172a;
#             font-size: 48px;
#             font-weight: 800;
#             line-height: 1;
#         }

#         .status-badge {
#             padding: 6px 12px;
#             border-radius: 99px;
#             font-size: 12px;
#             font-weight: 700;
#             background: #f1f5f9;
#             color: #475569;
#         }

#         .badge-critical { background: #fee2e2; color: #ef4444; }
#         .badge-evolving { background: #e0e7ff; color: #6366f1; }

#         /* Chart Styling */
#         .chart-container {
#             background: white;
#             padding: 1.5rem;
#             border-radius: 24px;
#             border: 1px solid #e2e8f0;
#         }

#         /* Selection Color Fix */
#         ::selection { background: #6366f1; color: white; }
#     </style>
# """, unsafe_allow_html=True)

# # --- UTILITIES ---
# def load_data(target_file_name: str):
#     out_dir = Path("cf_fuzz_output")
#     if not out_dir.exists(): return pd.DataFrame()
#     stem = Path(target_file_name).stem
#     csv_files = list(out_dir.glob(f"telemetry_{stem}_*.csv"))
#     if not csv_files: return pd.DataFrame()
#     return pd.read_csv(max(csv_files, key=os.path.getmtime))

# def render_pro_editor(code, vuln_line, filename):
#     lines = code.split('\n')
#     # Dark Mode Syntax Theme
#     html = f"""
#     <div style="background: #0f172a; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.2);">
#         <div style="background: #1e293b; padding: 12px 20px; display: flex; align-items: center; gap: 8px;">
#             <div style="width:12px; height:12px; border-radius:50%; background:#ff5f56"></div>
#             <div style="width:12px; height:12px; border-radius:50%; background:#ffbd2e"></div>
#             <div style="width:12px; height:12px; border-radius:50%; background:#27c93f"></div>
#             <span style="color: #94a3b8; font-family: 'JetBrains Mono'; font-size: 12px; margin-left: 10px;">{filename}</span>
#         </div>
#         <div style="height: 550px; overflow-y: auto; font-family: 'JetBrains Mono'; font-size: 13px; line-height: 1.6; padding: 10px 0;">
#     """
#     for i, line in enumerate(lines):
#         ln = i + 1
#         safe_line = line.replace('<', '&lt;').replace('>', '&gt;')
#         is_vuln = ln == vuln_line
#         bg = "rgba(239, 68, 68, 0.15)" if is_vuln else "transparent"
#         border = "2px solid #ef4444" if is_vuln else "2px solid transparent"
#         color = "#f8fafc" if not is_vuln else "#fca5a5"
        
#         html += f"""<div style="background: {bg}; border-left: {border}; padding: 0 20px; display: flex;">
#             <div style="width: 40px; color: #475569; user-select: none;">{ln}</div>
#             <div style="color: {color}; white-space: pre;">{safe_line}</div>
#             {"<span style='margin-left:auto; color:#ef4444; font-size:10px; font-weight:bold;'>VULNERABILITY</span>" if is_vuln else ""}
#         </div>"""
#     return html + "</div></div>"

# # --- SIDEBAR ---
# with st.sidebar:
#     st.markdown("<h1 style='font-size: 24px; font-weight: 800; color: #0f172a;'>CF-FUZZ <span style='color:#6366f1'>ULTRA</span></h1>", unsafe_allow_html=True)
#     st.markdown("---")
#     targets = {f.name: f for f in Path("dataset").glob("*.cpp")}
#     targets.update({f"✅ {f.name}": f for f in Path("dataset_success").glob("*.cpp")})
    
#     selected_name = st.selectbox("Select Target Explorer", list(targets.keys()))
#     live = st.toggle("Real-time Pulse", value=True)
#     if live: time.sleep(1); st.rerun()

# # --- MAIN UI ---
# path = targets[selected_name]
# code = path.read_text()
# df = load_data(path.name)

# # Extract vuln line from comments
# vuln_line = -1
# for line in code.splitlines()[:20]:
#     if "[VULN_LINE]" in line:
#         try: vuln_line = int(line.split(":")[-1].strip())
#         except: pass

# # 1. HEADER HERO BAR (The Super Amazing Part)
# peak_time = 0.0
# gen = 0
# if not df.empty:
#     peak_time = max(df['Island_Alpha_Peak_MS'].max(), df['Island_Beta_Peak_MS'].max(), df['Island_Gamma_Peak_MS'].max())
#     gen = df['Generation'].max()

# st.markdown(f"""
#     <div class="status-card">
#         <div>
#             <div class="metric-title">Live Peak Execution</div>
#             <div class="metric-value-huge">{peak_time:.1f}<span style="font-size: 20px; color: #94a3b8; margin-left: 5px;">ms</span></div>
#         </div>
#         <div style="text-align: center; border-left: 1px solid #e2e8f0; padding-left: 40px; margin-left: 40px;">
#             <div class="metric-title">Evolution Progress</div>
#             <div class="metric-value-huge">{gen}<span style="font-size: 20px; color: #94a3b8;">/30</span></div>
#         </div>
#         <div style="margin-left: auto;">
#             <span class="status-badge {'badge-critical' if peak_time > 1000 else 'badge-evolving'}">
#                 {'● CRITICAL SLOWDOWN' if peak_time > 1000 else '● OPTIMIZING PAYLOADS'}
#             </span>
#         </div>
#     </div>
# """, unsafe_allow_html=True)

# col_left, col_right = st.columns([1.2, 1], gap="large")

# with col_left:
#     st.markdown("<h3 style='font-weight:800; font-size:18px; color:#1e293b; margin-bottom:20px;'>Degradation Analysis</h3>", unsafe_allow_html=True)
#     if not df.empty:
#         df_m = df.melt(id_vars=['Generation'], value_vars=['Island_Alpha_Peak_MS', 'Island_Beta_Peak_MS', 'Island_Gamma_Peak_MS'], var_name='Island', value_name='ms')
#         df_m['Island'] = df_m['Island'].str.replace('Island_', '').str.replace('_Peak_MS', '')
        
#         fig = px.line(df_m, x='Generation', y='ms', color='Island', 
#                       color_discrete_map={"Alpha": "#ef4444", "Beta": "#6366f1", "Gamma": "#22c55e"})
#         fig.update_traces(line_shape='spline', line_width=4)
#         fig.update_layout(
#             hovermode="x unified", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
#             margin=dict(l=0, r=0, t=0, b=0), height=450,
#             xaxis=dict(showgrid=True, gridcolor="#f1f5f9", title="Generation"),
#             yaxis=dict(showgrid=True, gridcolor="#f1f5f9", title="CPU Time"),
#             legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
#         )
#         fig.add_hline(y=2000, line_dash="dash", line_color="#ef4444", annotation_text="TLE LIMIT")
#         st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# with col_right:
#     st.markdown("<h3 style='font-weight:800; font-size:18px; color:#1e293b; margin-bottom:20px;'>Intelligence Inspector</h3>", unsafe_allow_html=True)
#     st.markdown(render_pro_editor(code, vuln_line, path.name), unsafe_allow_html=True)








"""
CF-Fuzz Enterprise Analytics Dashboard.
Updated to fix KPI visibility, sizing, and remove complexity metric.
"""

import os
import time
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CF-Fuzz Analytics", layout="wide")

# --- ENTERPRISE SAAS CSS INJECTION ---
st.markdown("""
    <style>
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Force Pure Light Theme */
        .stApp { background-color: #FAFAFA !important; }
        
        /* Modern Typography */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: #111827 !important;
        }

        /* --- FIX: BIGGER METRICS & VISIBILITY --- */
        [data-testid="stMetricValue"] { 
            color: #0F172A !important; 
            font-weight: 800 !important; 
            font-size: 42px !important; /* Increased from 28px */
            line-height: 1.2 !important;
        }
        
        /* Fix the Metric Labels (Target, Peak Time, etc.) */
        [data-testid="stMetricLabel"] p {
            color: #64748B !important;
            font-size: 16px !important; /* Made labels bigger */
            font-weight: 600 !important;
            margin-bottom: 8px !important;
        }

        /* Metric Card Container Styling */
        div[data-testid="metric-container"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            padding: 24px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        }

        /* Fix Selection Highlight */
        ::selection {
            background: #635BFF;
            color: white;
        }

        /* Fix the Blackened Dropdown Boxes */
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #111827 !important;
            border: 1px solid #E2E8F0 !important;
        }
        
        [data-testid="stMetricDelta"] { 
            font-weight: 600 !important; 
            font-size: 14px !important;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADERS ---
@st.cache_data(ttl=1)
def load_telemetry_data(target_file_name: str, csv_dir="cf_fuzz_output") -> pd.DataFrame:
    out_dir = Path(csv_dir)
    if not out_dir.exists() or not target_file_name:
        return pd.DataFrame()
    stem = Path(target_file_name).stem
    csv_files = list(out_dir.glob(f"telemetry_{stem}_*.csv"))
    if not csv_files:
        return pd.DataFrame()
    latest_csv = max(csv_files, key=os.path.getmtime)
    try:
        return pd.read_csv(latest_csv)
    except Exception:
        return pd.DataFrame()

def extract_metadata(code_content: str) -> dict:
    meta = {"TRAP_CATEGORY": "Uncategorized Algorithm", "VULN_LINE": -1}
    for line in code_content.splitlines()[:20]:
        if "[TRAP_CATEGORY]" in line: meta["TRAP_CATEGORY"] = line.split(":")[-1].strip()
        elif "[VULN_LINE]" in line: 
            try: meta["VULN_LINE"] = int(line.split(":")[-1].strip())
            except: pass
    return meta

def render_highlighted_code(code_str: str, vuln_line: int, filename: str):
    lines = code_str.split('\n')
    html = f"""<div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); overflow: hidden; margin-bottom: 20px;">
<div style="background-color: #F8FAFC; padding: 12px 16px; border-bottom: 1px solid #E2E8F0; display: flex; align-items: center;">
<div style="width: 12px; height: 12px; background-color: #FF5F56; border-radius: 50%; margin-right: 8px;"></div>
<div style="width: 12px; height: 12px; background-color: #FFBD2E; border-radius: 50%; margin-right: 8px;"></div>
<div style="width: 12px; height: 12px; background-color: #27C93F; border-radius: 50%; margin-right: 16px;"></div>
<span style="font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #64748B; font-weight: 600;">{filename}</span>
</div>
<div style="height: 480px; overflow-y: auto; padding: 12px 0; background-color: #FFFFFF; font-family: 'JetBrains Mono', monospace; font-size: 13px; line-height: 1.6;">"""
    for i, line in enumerate(lines):
        line_num = i + 1
        safe_line = line.replace('<', '&lt;').replace('>', '&gt;')
        if line_num == vuln_line:
            html += f"<div style=\"background-color: #FEF2F2; border-left: 4px solid #EF4444; display: flex; padding: 2px 0;\"><div style=\"width: 45px; text-align: right; padding-right: 15px; color: #EF4444; font-weight: bold; user-select: none;\">{line_num}</div><div style=\"color: #991B1B; font-weight: 700;\">{safe_line} <span style=\"color: #EF4444; margin-left: 15px; font-size: 11px;\">&lt;-- EXPLOITED BOTTLENECK</span></div></div>"
        else:
            html += f"<div style=\"display: flex; padding: 0;\"><div style=\"width: 45px; text-align: right; padding-right: 15px; color: #CBD5E1; user-select: none;\">{line_num}</div><div style=\"color: #334155;\">{safe_line}</div></div>"
    html += "</div></div>"
    return html

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#0F172A; font-weight:900; margin-bottom:0;'>CF-Fuzz</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-weight:500; margin-top:0;'>Automated AlgoDoS Discovery</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    targets = {}
    if Path("dataset").exists():
        for f in Path("dataset").glob("*.cpp"): targets[f"Pending: {f.name}"] = f
    if Path("dataset_success").exists():
        for f in Path("dataset_success").glob("*.cpp"): targets[f"Hacked: {f.name}"] = f
    st.markdown("<p style='font-size: 14px; font-weight: 600; color: #334155; margin-bottom: 5px;'>Target Repository</p>", unsafe_allow_html=True)
    selected_display = st.selectbox("", list(targets.keys()), label_visibility="collapsed") if targets else None
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.toggle("Live Telemetry Sync", value=False):
        time.sleep(1)
        st.rerun()

# --- MAIN DASHBOARD ---
if not selected_display:
    st.info("Please select a target from the sidebar.")
    st.stop()

code_path = targets[selected_display]
code_content = code_path.read_text(encoding='utf-8')
meta = extract_metadata(code_content)
df = load_telemetry_data(code_path.name)

# 1. UPDATED KPI ROW (Removed Expected Complexity, Increased Column Width)
# 1. UPDATED KPI ROW
kpi1, kpi2, _ = st.columns([1, 1, 1])  # 3 columns layout keeps cards compact on the left side

current_gen = df['Generation'].max() if not df.empty else 0
global_peak = 0
if not df.empty:
    global_peak = max(df['Island_Alpha_Peak_MS'].max(), df['Island_Beta_Peak_MS'].max(), df['Island_Gamma_Peak_MS'].max())

kpi1.metric("Peak Execution Time", f"{global_peak:.1f} ms", 
            delta="Critical Degradation" if global_peak > 500 else "Stable Baseline", 
            delta_color="inverse")
kpi2.metric("Evolutionary Epoch", f"Gen {current_gen} / 30")

# kpi1, kpi2, kpi3 = st.columns(3)

# current_gen = df['Generation'].max() if not df.empty else 0
# global_peak = 0
# if not df.empty:
#     global_peak = max(df['Island_Alpha_Peak_MS'].max(), df['Island_Beta_Peak_MS'].max(), df['Island_Gamma_Peak_MS'].max())

# # kpi1.metric("Vulnerability Target", meta["TRAP_CATEGORY"])
# kpi2.metric("Peak Execution Time", f"{global_peak:.1f} ms", 
#             delta="Critical Degradation" if global_peak > 500 else "Stable Baseline", 
#             delta_color="inverse")
# kpi3.metric("Evolutionary Epoch", f"Gen {current_gen} / 30")

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# 2. MAIN VISUALS
col_graph, col_code = st.columns([0.55, 0.45], gap="large")

with col_graph:
    st.markdown("<h4 style='color:#0F172A; font-weight: 700;'>Degradation Trajectory</h4>", unsafe_allow_html=True)
    if not df.empty:
        df_melted = df.melt(id_vars=['Generation'], value_vars=['Island_Alpha_Peak_MS', 'Island_Beta_Peak_MS', 'Island_Gamma_Peak_MS'], var_name='Genetic Island', value_name='CPU_Time_MS')
        df_melted['Genetic Island'] = df_melted['Genetic Island'].str.replace('_Peak_MS', '').str.replace('Island_', '')
        fig = px.line(df_melted, x="Generation", y="CPU_Time_MS", color='Genetic Island', color_discrete_map={"Alpha": "#FF4F40", "Beta": "#635BFF", "Gamma": "#00D924"})
        fig.update_traces(line_shape='spline', line_width=3)
        fig.update_layout(plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", height=500, margin=dict(l=0, r=0, t=10, b=0))
        fig.add_hline(y=2000, line_dash="dash", line_color="#EF4444", annotation_text="OS TLE Limit")
        st.plotly_chart(fig, use_container_width=True)

with col_code:
    st.markdown("<h4 style='color:#0F172A; font-weight: 700;'>Source Inspector</h4>", unsafe_allow_html=True)
    st.markdown(render_highlighted_code(code_content, meta["VULN_LINE"], code_path.name), unsafe_allow_html=True)