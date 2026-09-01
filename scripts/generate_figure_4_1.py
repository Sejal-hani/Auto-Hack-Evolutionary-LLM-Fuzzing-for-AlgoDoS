"""
Generates the publication-quality Figure 4.1:
'Figure 4.1: Punctuated Equilibrium Trajectory on victim_002_dp.cpp'
Using Plotly to match the exact colors, markers, line styles, grid, and legend.
"""

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# Paths
repo_root = Path(__file__).resolve().parent.parent
csv_path = repo_root / "cf_fuzz_output" / "telemetry_victim_002_dp.cpp.csv"
output_html = repo_root / "cf_fuzz_output" / "figure_4_1_punctuated_equilibrium.html"

df = pd.read_csv(csv_path)

fig = go.Figure()

# Island Alpha (Extremist) - Red solid line with circle markers
fig.add_trace(go.Scatter(
    x=df['Generation'],
    y=df['Delta_Extremist'],
    mode='lines+markers',
    name='Island Alpha (Extremist)',
    line=dict(color='#FF0000', width=2.5),
    marker=dict(symbol='circle', size=9, color='#FF0000')
))

# Island Beta (Duplicator) - Blue dashed line with square markers
fig.add_trace(go.Scatter(
    x=df['Generation'],
    y=df['Beta_AllEqual'],
    mode='lines+markers',
    name='Island Beta (Duplicator)',
    line=dict(color='#0033FF', width=2.5, dash='dash'),
    marker=dict(symbol='square', size=9, color='#0033FF')
))

# Time Limit Exceeded Threshold (2000 ms) - Red dotted line
fig.add_hline(
    y=2000, line_dash='dot', line_color='#FF0033', line_width=1.8,
    annotation_text='Time Limit Exceeded Threshold (2000 ms)',
    annotation_position='top left',
    annotation_font_color='#FF0033'
)

fig.update_layout(
    title=dict(text="Figure 4.1: Punctuated Equilibrium Trajectory on victim_002_dp.cpp", font=dict(size=14, color="#FFFFFF")),
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0.2)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        showgrid=True, gridcolor="#333333", gridwidth=1,
        title="Evolutionary Generation",
        dtick=0.5, range=[0.8, 5.2]
    ),
    yaxis=dict(
        showgrid=True, gridcolor="#333333", gridwidth=1,
        title="CPU User Time (ms)",
        range=[-50, 2150], dtick=250
    ),
    legend=dict(
        x=0.02, y=0.55,
        bgcolor="rgba(0,0,0,0.6)",
        bordercolor="#444",
        borderwidth=1
    ),
    width=800,
    height=480,
    margin=dict(l=50, r=30, t=50, b=50)
)

fig.write_html(str(output_html))
print(f"[OK] Figure 4.1 successfully generated and saved to: {output_html}")
