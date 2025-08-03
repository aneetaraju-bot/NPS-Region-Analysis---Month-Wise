import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 NPS & Responses - Vertical-wise (Region Filtered)")

uploaded_file = st.file_uploader("📥 Upload your NPS CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Fill missing vertical & region
    df[['Vertical', 'Region']] = df[['Vertical', 'Region']].fillna(method='ffill')

    try:
        df = df[['Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses']]
    except KeyError:
        st.error("CSV must contain: 'Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses'")
        st.stop()

    # Rename
    df.columns = ['Vertical', 'Region', 'Status', 'NPS_Score', 'Responses']
    df.dropna(subset=['NPS_Score', 'Responses'], inplace=True)
    df['NPS_Score'] = pd.to_numeric(df['NPS_Score'], errors='coerce')
    df['Responses'] = pd.to_numeric(df['Responses'], errors='coerce')

    # Filter by region
    regions = df['Region'].unique()
    selected_region = st.selectbox("🌍 Select Region", sorted(regions))
    region_df = df[df['Region'] == selected_region].copy()

    # Build label & plot
    region_df['Label'] = region_df['Vertical']
    labels = region_df['Label'].unique()
    statuses = region_df['Status'].unique()

    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(labels))
    width = 0.25

    color_map = {'Beginner Batches': 'royalblue', 'Mid Course Batches': 'orange', 'End Month Batches': 'seagreen'}

    for idx, status in enumerate(statuses):
        data = region_df[region_df['Status'] == status]
        bar_positions = x + (idx - len(statuses)/2) * width
        bars = ax.bar(bar_positions, data['NPS_Score'], width=width, label=status, color=color_map.get(status, 'gray'))

        for i, bar in enumerate(bars):
            score = data['NPS_Score'].values[i]
            responses = int(data['Responses'].values[i])
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f"{score:.1f}%\n{responses}R", ha='center', fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel("NPS Score (%)")
    ax.set_ylim(0, max(region_df['NPS_Score'].max() + 20, 100))
    ax.set_title(f"NPS Score by Vertical – {selected_region}")
    ax.legend(title="Batch Status")

    st.pyplot(fig)

else:
    st.info("📁 Please upload a CSV file with headers: Vertical, Region, Status, NPS Score %, SUM of No: of Responses")
