# updated the app.py for test dataset 

"""
CF-Fuzz Minimalist Telemetry Dashboard (Dynamic Edition).

Reads real-time CSV outputs from the evolutionary engine.
Dynamically populates the target list from the dataset/ directory.
"""

import os
import time
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CF-Fuzz | AlgoDoS Telemetry", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        * { font-family: 'Courier New', Courier, monospace !important; }
        .stButton>button { width: 100%; border-radius: 0px; border: 1px solid #00FF00; color: #00FF00; background-color: #000000; }
        .stButton>button:hover { background-color: #00FF00; color: #000000; }
    </style>
""", unsafe_allow_html=True)


# --- DATA LOADERS ---
@st.cache_data(ttl=1) # Cache clears every 1 second to fetch live data
def load_telemetry_data(target_file_name: str, csv_dir="cf_fuzz_output") -> pd.DataFrame:
    """Finds the most recent CSV log FOR THE SELECTED VICTIM and loads it."""
    out_dir = Path(csv_dir)
    if not out_dir.exists() or not target_file_name:
        return pd.DataFrame()
        
    # Match the CSV file to the selected C++ file
    stem = Path(target_file_name).stem
    csv_files = list(out_dir.glob(f"telemetry_{stem}_*.csv"))
    
    if not csv_files:
        return pd.DataFrame()
        
    latest_csv = max(csv_files, key=os.path.getmtime)
    try:
        return pd.read_csv(latest_csv)
    except Exception:
        return pd.DataFrame()

# --- MAIN UI LAYOUT ---
st.markdown("### `CF-FUZZ :: ASYMPTOTIC VULNERABILITY DISCOVERY ENGINE`")
st.markdown("---")

col_target, col_telem = st.columns([0.3, 0.7])

with col_target:
    st.markdown("#### `TARGET_CONFIG`")
    
    # DYNAMICALLY LOAD FROM DATASET DIRECTORY
    dataset_dir = Path("dataset")
    if dataset_dir.exists():
        available_targets = [f.name for f in dataset_dir.glob("*.cpp")]
    else:
        available_targets = []
        
    if not available_targets:
        target_file = st.selectbox("Select Codeforces Victim:", ["No files found in dataset/"])
    else:
        target_file = st.selectbox("Select Codeforces Victim:", available_targets)
    
    st.markdown("##### `SOURCE_CODE`")
    
    # Dynamically display the code of the selected file
    if target_file and target_file != "No files found in dataset/":
        code_path = dataset_dir / target_file
        if code_path.exists():
            code_content = code_path.read_text(encoding='utf-8')
            # Show the first 30 lines so it doesn't clutter the screen
            preview = "\n".join(code_content.splitlines()[:30]) + "\n// ... [TRUNCATED] ..."
            st.code(preview, language="cpp")
    
    if st.button("EXECUTE FUZZ_ORCHESTRATOR()"):
        st.toast("Use the batch runner in the terminal to execute!", icon="⚡")


with col_telem:
    st.markdown("#### `HARDWARE_TELEMETRY (LIVE)`")
    dashboard_placeholder = st.empty()
    
    # UI Render Loop
    for _ in range(5): 
        df = load_telemetry_data(target_file)
        
        with dashboard_placeholder.container():
            if df.empty:
                st.warning(f"Awaiting Fuzzer connection... No CSV telemetry found for {target_file}.")
            else:
                metric1, metric2, metric3 = st.columns(3)
                max_beta = df['Island_Beta_Peak_MS'].max() if not df.empty else 0
                current_gen = df['Generation'].max() if not df.empty else 0
                status = df['Status'].iloc[-1] if not df.empty else "UNKNOWN"
                
                metric1.metric("Current Generation", f"{current_gen} / 30")
                metric2.metric("Peak CPU Time", f"{max_beta} ms", delta="Tracking" if status != "TLE_ACHIEVED" else "CRASHED", delta_color="inverse")
                metric3.metric("System Status", status)
                
                st.markdown("##### `ALGODOS_DEGRADATION_CURVE`")
                df_melted = df.melt(id_vars=['Generation'], value_vars=['Island_Alpha_Peak_MS', 'Island_Beta_Peak_MS', 'Island_Gamma_Peak_MS'], var_name='Island', value_name='CPU_Time_MS')
                
                fig = px.line(df_melted, x="Generation", y="CPU_Time_MS", color='Island', color_discrete_map={"Island_Alpha_Peak_MS": "#FF3366", "Island_Beta_Peak_MS": "#33CCFF", "Island_Gamma_Peak_MS": "#00FF66"})
                
                # Dynamic Y-Axis scale based on the data
                max_y = max(2200, df_melted['CPU_Time_MS'].max() + 200) if not df_melted.empty else 2200

                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=False, zeroline=False, title="EVOLUTIONARY GENERATION"),
                    yaxis=dict(showgrid=True, gridcolor="#333333", zeroline=False, title="CPU USER TIME (ms)", range=[0, max_y]),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                fig.add_hline(y=2000, line_dash="dot", line_color="#FF0000", annotation_text="OS TLE LIMIT (2000ms)")
                
                st.plotly_chart(fig, use_container_width=True)
                
        time.sleep(1)


# """
# CF-Fuzz Minimalist Telemetry Dashboard.

# Pure performance UI. No clutter.
# Reads real-time CSV outputs from the evolutionary engine and plots asymptotic degradation.
# Designed for high-density data visualization during thesis defense.
# """

# import os
# import time
# import pandas as pd
# import streamlit as st
# import plotly.express as px
# from pathlib import Path

# # --- PAGE CONFIGURATION (Minimalist & Wide) ---
# st.set_page_config(
#     page_title="CF-Fuzz | AlgoDoS Telemetry",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Force dark mode and hide Streamlit default UI elements (hamburger menu, footer)
# st.markdown("""
#     <style>
#         #MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#         header {visibility: hidden;}
#         /* Minimalist Monospace font for that terminal feel */
#         * { font-family: 'Courier New', Courier, monospace !important; }
#         .stButton>button { width: 100%; border-radius: 0px; border: 1px solid #00FF00; color: #00FF00; background-color: #000000; }
#         .stButton>button:hover { background-color: #00FF00; color: #000000; }
#     </style>
# """, unsafe_allow_html=True)


# # --- DATA LOADERS ---
# @st.cache_data(ttl=1) # Cache clears every 1 second to fetch live data
# def load_telemetry_data(csv_dir="cf_fuzz_output") -> pd.DataFrame:
#     """Finds the most recent CSV log and loads it for visualization."""
#     out_dir = Path(csv_dir)
#     if not out_dir.exists():
#         return pd.DataFrame()
        
#     csv_files = list(out_dir.glob("telemetry_*.csv"))
#     if not csv_files:
#         return pd.DataFrame()
        
#     # Get the latest run
#     latest_csv = max(csv_files, key=os.path.getmtime)
#     try:
#         df = pd.read_csv(latest_csv)
#         return df
#     except Exception:
#         return pd.DataFrame()

# # --- MAIN UI LAYOUT ---
# st.markdown("### `CF-FUZZ :: ASYMPTOTIC VULNERABILITY DISCOVERY ENGINE`")
# st.markdown("---")

# # Split screen: 30% Target, 70% Telemetry
# col_target, col_telem = st.columns([0.3, 0.7])

# with col_target:
#     st.markdown("#### `TARGET_CONFIG`")
    
#     # Mock dropdown for your Codeforces datasets
#     target_file = st.selectbox("Select Codeforces Victim:", ["victim_quicksort.cpp", "victim_dfs_graph.cpp", "victim_hashmap.cpp"])
    
#     st.markdown("##### `AST_METADATA_INJECTED`")
#     st.code("""
# {
#     "max_loop_depth": 2,
#     "recursive_functions": [],
#     "vulnerable_stls": ["std::unordered_map"]
# }
#     """, language="json")
    
#     # Normally you'd read the actual C++ file here
#     st.markdown("##### `SOURCE_CODE`")
#     st.code("""
# // Vulnerable Codeforces Submission
# #include <iostream>
# #include <unordered_map>
# using namespace std;

# int main() {
#     int N; cin >> N;
#     unordered_map<int, int> freq;
#     for(int i=0; i<N; i++) {
#         int x; cin >> x;
#         freq[x]++; // VULNERABILITY: Hash Collision Trap
#     }
#     cout << freq.size();
# }
#     """, language="cpp")
    
#     if st.button("EXECUTE FUZZ_ORCHESTRATOR()"):
#         # In a full deployment, this button would trigger main_loop.py via subprocess.
#         # For the UI, we just notify the user.
#         st.toast("Initialization signal sent to OS Sandbox.", icon="⚡")


# with col_telem:
#     st.markdown("#### `HARDWARE_TELEMETRY (LIVE)`")
    
#     # The Placeholder allows us to overwrite this specific UI block in a loop
#     dashboard_placeholder = st.empty()
    
#     # Simulating a real-time polling loop
#     for _ in range(10): # In reality, you can wrap this in a while True loop during the live demo
#         df = load_telemetry_data()
        
#         with dashboard_placeholder.container():
#             if df.empty:
#                 st.warning("Awaiting Fuzzer connection... No CSV telemetry found.")
#             else:
#                 # Top KPI Metrics
#                 metric1, metric2, metric3 = st.columns(3)
                
#                 # Extract max values safely
#                 max_alpha = df['Island_Alpha_Peak_MS'].max() if not df.empty else 0
#                 max_beta = df['Island_Beta_Peak_MS'].max() if not df.empty else 0
#                 current_gen = df['Generation'].max() if not df.empty else 0
#                 status = df['Status'].iloc[-1] if not df.empty else "UNKNOWN"
                
#                 metric1.metric("Current Generation", f"{current_gen} / 30")
#                 metric2.metric("Peak CPU Time (Island Beta)", f"{max_beta} ms", delta="Tracking" if status != "TLE_ACHIEVED" else "CRASHED", delta_color="inverse")
#                 metric3.metric("System Status", status)
                
#                 # --- Plotly Exponential Curve Graph ---
#                 st.markdown("##### `ALGODOS_DEGRADATION_CURVE`")
                
#                 # Melt the dataframe so Plotly can draw multiple lines easily
#                 df_melted = df.melt(
#                     id_vars=['Generation'], 
#                     value_vars=['Island_Alpha_Peak_MS', 'Island_Beta_Peak_MS', 'Island_Gamma_Peak_MS'],
#                     var_name='Island', 
#                     value_name='CPU_Time_MS'
#                 )
                
#                 # Build the minimalist chart
#                 fig = px.line(
#                     df_melted, x="Generation", y="CPU_Time_MS", color='Island',
#                     color_discrete_map={
#                         "Island_Alpha_Peak_MS": "#FF3366", # Aggressive Red
#                         "Island_Beta_Peak_MS": "#33CCFF",  # Cyber Blue
#                         "Island_Gamma_Peak_MS": "#00FF66"  # Matrix Green
#                     }
#                 )
                
#                 # Strip all gridlines and backgrounds for the "Quant Terminal" look
#                 fig.update_layout(
#                     plot_bgcolor="rgba(0,0,0,0)",
#                     paper_bgcolor="rgba(0,0,0,0)",
#                     xaxis=dict(showgrid=False, zeroline=False, title="EVOLUTIONARY GENERATION"),
#                     yaxis=dict(showgrid=True, gridcolor="#333333", zeroline=False, title="CPU USER TIME (ms)", range=[0, 2200]),
#                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#                     margin=dict(l=0, r=0, t=0, b=0)
#                 )
                
#                 # Draw the hard 2000ms TLE limit line
#                 fig.add_hline(y=2000, line_dash="dot", line_color="#FF0000", annotation_text="OS TLE LIMIT (2000ms)")
                
#                 # Render the chart
#                 st.plotly_chart(fig, use_container_width=True)
                
#         # Briefly sleep to prevent locking the browser thread
#         time.sleep(1)