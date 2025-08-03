import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 ML Region Categories - NPS & Responses Evaluation")

uploaded_file = st.file_uploader("📥 Upload your NPS CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Fill missing vertical & region
    df[['Vertical', 'Region']] = df[['Vertical', 'Region']].fillna(method='ffill')

    # Clean column names
    try:
        df = df[['Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses']]
    except KeyError:
        st.error("CSV must contain: 'Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses'")
        st.stop()

    # Rename and convert
    df.columns = ['Vertical', 'Region', 'Status', 'NPS_Score', 'Responses']
    df.dropna(subset=['NPS_Score', 'Responses'], inplace=True)
    df['NPS_Score'] = pd.to_numeric(df['NPS_Score'], errors='coerce')
    df['Responses'] = pd.to_numeric(df['Responses'], errors='coerce')

    # Region selector
    regions = df['Region'].unique()
    selected_region = st.selectbox("🌍 Select Region", sorted(regions))

    region_df = df[df['Region'] == selected_region].copy()
    region_df['Label'] = region_df['Vertical'] + " (" + region_df['Status'] + ")"

    # Set up positions for grouped bars
    x = np.arange(len(region_df))
    width = 0.4

    fig, ax1 = plt.subplots(figsize=(16, 6))
    ax2 = ax1.twinx()

    # Bars
    bars1 = ax1.bar(x - width/2, region_df['NPS_Score'], width, label='NPS Score', color='royalblue')
    bars2 = ax2.bar(x + width/2, region_df['Responses'], width, label='No. of Responses', color='seagreen')

    # Labels on top of bars
    for i in range(len(region_df)):
        ax1.text(x[i] - width/2, region_df['NPS_Score'].iloc[i] + 2, f"{region_df['NPS_Score'].iloc[i]:.1f}%", ha='center', fontsize=9)
        ax2.text(x[i] + width/2, region_df['Responses'].iloc[i] + 2, f"{int(region_df['Responses'].iloc[i])}", ha='center', fontsize=9)

    # Axis settings
    ax1.set_ylabel("NPS Score (%)", color='royalblue')
    ax2.set_ylabel("No. of Responses", color='seagreen')
    ax1.set_ylim(0, max(region_df['NPS_Score'].max() + 20, 100))
    ax2.set_ylim(0, region_df['Responses'].max() + 15)

    ax1.set_xticks(x)
    ax1.set_xticklabels(region_df['Label'], rotation=30, ha='right', fontsize=9)

    fig.tight_layout()
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=2)
    ax1.set_title(f"NPS Score vs. Responses – {selected_region}", fontsize=14)

    st.pyplot(fig)

else:
    st.info("📁 Upload a CSV with columns: Vertical, Region, Status, NPS Score %, SUM of No: of Responses")
