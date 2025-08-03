import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 NPS Score & Responses by Vertical (Region-wise)")

uploaded_file = st.file_uploader("📥 Upload your NPS CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    df[['Vertical', 'Region']] = df[['Vertical', 'Region']].fillna(method='ffill')

    try:
        df = df[['Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses']]
    except KeyError:
        st.error("CSV must contain: 'Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses'")
        st.stop()

    df.columns = ['Vertical', 'Region', 'Status', 'NPS_Score', 'Responses']
    df.dropna(subset=['NPS_Score', 'Responses'], inplace=True)
    df['NPS_Score'] = pd.to_numeric(df['NPS_Score'], errors='coerce')
    df['Responses'] = pd.to_numeric(df['Responses'], errors='coerce')

    # Select Region
    regions = df['Region'].unique()
    selected_region = st.selectbox("🌍 Select Region", sorted(regions))
    region_df = df[df['Region'] == selected_region].copy()

    # X-axis: unique verticals
    verticals = region_df['Vertical'].unique()
    statuses = ['Beginner Batches', 'Mid Course Batches', 'End Month Batches']
    color_map = {'Beginner Batches': 'royalblue', 'Mid Course Batches': 'orange', 'End Month Batches': 'seagreen'}

    x = np.arange(len(verticals))
    width = 0.2

    fig, ax = plt.subplots(figsize=(16, 6))

    for i, status in enumerate(statuses):
        scores = []
        counts = []
        for vert in verticals:
            match = region_df[(region_df['Vertical'] == vert) & (region_df['Status'] == status)]
            if not match.empty:
                scores.append(match['NPS_Score'].values[0])
                counts.append(int(match['Responses'].values[0]))
            else:
                scores.append(0)
                counts.append(0)

        bar_x = x + (i - 1) * width
        bars = ax.bar(bar_x, scores, width=width, label=status, color=color_map.get(status, 'gray'))

        for j, bar in enumerate(bars):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                    f"{scores[j]:.1f}%\n{counts[j]}R",
                    ha='center', fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(verticals, rotation=45, ha='right')
    ax.set_ylabel("NPS Score (%)")
    ax.set_ylim(0, max(region_df['NPS_Score'].max() + 20, 100))
    ax.set_title(f"NPS Scores by Vertical – {selected_region}")
    ax.legend(title="Batch Status")

    st.pyplot(fig)

else:
    st.info("📁 Upload a CSV with columns: Vertical, Region, Status, NPS Score %, SUM of No: of Responses")
