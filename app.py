import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 Cumulative NPS Score & Responses by Vertical (Grouped by Status)")

uploaded_file = st.file_uploader("📥 Upload your NPS CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Fill missing values in Vertical & Region
    df[['Vertical', 'Region']] = df[['Vertical', 'Region']].fillna(method='ffill')

    # Select only required columns
    try:
        df = df[['Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses']]
    except KeyError:
        st.error("CSV must contain: 'Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses'")
        st.stop()

    # Rename columns
    df.columns = ['Vertical', 'Region', 'Status', 'NPS_Score', 'Responses']
    df.dropna(subset=['NPS_Score', 'Responses'], inplace=True)
    df['NPS_Score'] = pd.to_numeric(df['NPS_Score'], errors='coerce')
    df['Responses'] = pd.to_numeric(df['Responses'], errors='coerce')

    # ✅ Normalize Status values to 3 standard groups
    status_mapping = {
        'Elevate Beginner Batch': 'Beginner Batches',
        'Beginner Batches': 'Beginner Batches',
        'Mid Level Batches': 'Mid Course Batches',
        'Elevate Mid Level': 'Mid Course Batches',
        'End Month Batches': 'End Month Batches',
        'Elevate End Month': 'End Month Batches'
    }
    df['Status'] = df['Status'].map(status_mapping)
    df = df.dropna(subset=['Status'])

    # ✅ Cumulative aggregation by Vertical + Region + Status
    df_grouped = df.groupby(['Vertical', 'Region', 'Status'], as_index=False).agg({
        'NPS_Score': 'mean',
        'Responses': 'sum'
    })

    # Region filter
    regions = df_grouped['Region'].dropna().unique()
    selected_region = st.selectbox("🌍 Select Region", sorted(regions))

    region_df = df_grouped[df_grouped['Region'] == selected_region].copy()

    verticals = sorted(region_df['Vertical'].unique())
    statuses = ['Beginner Batches', 'Mid Course Batches', 'End Month Batches']

    x = np.arange(len(verticals))
    width = 0.25
    color_map = {
        'Beginner Batches': 'royalblue',
        'Mid Course Batches': 'orange',
        'End Month Batches': 'seagreen'
    }

    # Plotting
    fig, ax = plt.subplots(figsize=(16, 6))

    for i, status in enumerate(statuses):
        scores = []
        responses = []

        for vert in verticals:
            row = region_df[(region_df['Vertical'] == vert) & (region_df['Status'] == status)]
            if not row.empty:
                scores.append(row['NPS_Score'].values[0])
                responses.append(int(row['Responses'].values[0]))
            else:
                scores.append(0)
                responses.append(0)

        bar_x = x + (i - 1) * width
        bars = ax.bar(bar_x, scores, width=width, label=status, color=color_map.get(status, 'gray'))

        # ✅ Always show labels, even for 0 or negative
        for j, bar in enumerate(bars):
            y_offset = 1 if scores[j] >= 0 else -4
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + y_offset,
                f"{scores[j]:.1f}%\n{responses[j]}R",
                ha='center',
                fontsize=8
            )

    ax.set_xticks(x)
    ax.set_xticklabels(verticals, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel("NPS Score (%)")

    # ✅ Adjust y-axis to show negatives and all bars
    min_score = min(region_df['NPS_Score'].min(), 0)
    max_score = max(region_df['NPS_Score'].max(), 100)
    ax.set_ylim(min_score - 10, max_score + 10)

    ax.set_title(f"📊 Cumulative NPS by Vertical – {selected_region}")
    ax.legend(title="Batch Status", bbox_to_anchor=(1.02, 1), loc='upper left')

    st.pyplot(fig)

else:
    st.info("📁 Please upload a CSV file with columns: Vertical, Region, Status, NPS Score %, SUM of No: of Responses")
