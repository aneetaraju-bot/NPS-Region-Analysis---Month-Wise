import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Region-wise NPS Evaluation by Vertical")

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

    df.columns = ['Vertical', 'Region', 'Status', 'NPS_Score', 'Responses']
    df.dropna(subset=['NPS_Score', 'Responses'], inplace=True)
    df['NPS_Score'] = pd.to_numeric(df['NPS_Score'], errors='coerce')
    df['Responses'] = pd.to_numeric(df['Responses'], errors='coerce')

    # Region filter
    regions = df['Region'].unique()
    selected_region = st.selectbox("Select Region", sorted(regions))

    # Filter by selected region
    region_df = df[df['Region'] == selected_region].copy()

    # Label = Vertical + Status
    region_df['Label'] = region_df['Vertical'] + " (" + region_df['Status'] + ")"

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(region_df['Label'], region_df['NPS_Score'], color='cornflowerblue')

    # Add values on top of bars
    for i, bar in enumerate(bars):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        nps = f"{region_df['NPS_Score'].iloc[i]:.1f}%"
        responses = f"{int(region_df['Responses'].iloc[i])} responses"
        ax.text(x, y + 2, nps, ha='center', fontsize=9)
        ax.text(x, y + 7, responses, ha='center', fontsize=8, color='gray')

    ax.set_title(f"NPS Score – {selected_region} Region", fontsize=14)
    ax.set_ylabel("NPS Score (%)")
    ax.set_ylim(0, max(region_df['NPS_Score'].max() + 15, 100))
    ax.set_xticklabels(region_df['Label'], rotation=30, ha='right', fontsize=9)

    st.pyplot(fig)
else:
    st.info("Upload a CSV with columns: Vertical, Region, Status, NPS Score %, SUM of No: of Responses")
