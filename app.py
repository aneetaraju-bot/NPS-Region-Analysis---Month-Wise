import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 NPS Evaluation – Region-wise Vertical Breakdown")

uploaded_file = st.file_uploader("Upload your NPS CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Fill missing values
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

    regions = df['Region'].dropna().unique()
    selected_region = st.selectbox("Select Region", options=sorted(regions))

    filtered_df = df[df['Region'] == selected_region].copy()

    # Label = only Vertical - Region
    filtered_df['Label'] = filtered_df['Vertical'] + " - " + filtered_df['Region']
    filtered_df.sort_values(by='Vertical', inplace=True)

    fig, ax = plt.subplots(figsize=(14, 6))
    x = range(len(filtered_df))

    bars = ax.bar(x, filtered_df['NPS_Score'], color='cornflowerblue', width=0.5)

    for i, bar in enumerate(bars):
        yval = bar.get_height()
        label_x = bar.get_x() + bar.get_width() / 2

        # Add NPS + Responses on top
        nps_val = f"{filtered_df['NPS_Score'].values[i]:.1f}%"
        responses_val = f"{int(filtered_df['Responses'].values[i])} responses"
        ax.text(label_x, yval + 2, nps_val, ha='center', fontsize=10)
        ax.text(label_x, yval + 7, responses_val, ha='center', fontsize=9, color='gray')

        # Add status to the left side
        ax.text(bar.get_x() - 0.1, yval / 2, filtered_df['Status'].values[i],
                ha='right', va='center', fontsize=9, color='black')

    ax.set_xticks(x)
    ax.set_xticklabels(filtered_df['Label'], rotation=45, ha='right')
    ax.set_ylabel("NPS Score (%)")
    ax.set_title(f"NPS Score by Vertical – {selected_region}")
    ax.set_ylim(0, max(filtered_df['NPS_Score'].max() + 15, 100))

    st.pyplot(fig)
else:
    st.info("📁 Please upload a CSV file to begin.")
