import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 ML Region Categories - NPS Evaluation")

uploaded_file = st.file_uploader("📁 Upload your NPS CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Fill missing values
    df[['Vertical', 'Region']] = df[['Vertical', 'Region']].fillna(method='ffill')

    # Rename and clean
    try:
        df = df[['Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses']]
    except KeyError:
        st.error("❌ CSV must contain: 'Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses'")
        st.stop()

    df.columns = ['Vertical', 'Region', 'Status', 'NPS_Score', 'Responses']
    df.dropna(subset=['NPS_Score', 'Responses'], inplace=True)
    df['NPS_Score'] = pd.to_numeric(df['NPS_Score'], errors='coerce')
    df['Responses'] = pd.to_numeric(df['Responses'], errors='coerce')

    # Add combined label
    df['Label'] = df['Vertical'] + " - " + df['Region']
    df.sort_values(by='Label', inplace=True)

    # Plot
    fig, ax1 = plt.subplots(figsize=(16, 6))
    x = range(len(df))

    # Blue bar - NPS Score
    bars1 = ax1.bar(x, df['NPS_Score'], width=0.4, color='royalblue', label='NPS Score')

    # Right Y-axis - Green bar - No. of Responses
    ax2 = ax1.twinx()
    bars2 = ax2.bar([i + 0.4 for i in x], df['Responses'], width=0.4, color='seagreen', label='No. of Responses')

    # Labels and values
    for i, (b1, b2) in enumerate(zip(bars1, bars2)):
        label_x1 = b1.get_x() + b1.get_width() / 2
        label_x2 = b2.get_x() + b2.get_width() / 2

        # Top of bars
        ax1.text(label_x1, b1.get_height() + 2, f"{df['NPS_Score'].iloc[i]:.2f}", ha='center', fontsize=8, color='blue')
        ax2.text(label_x2, b2.get_height() + 2, f"{int(df['Responses'].iloc[i])}", ha='center', fontsize=8, color='green')

        # Left-side label (Status)
        ax1.text(b1.get_x() - 0.2, b1.get_height() / 2, df['Status'].iloc[i], ha='right', va='center', fontsize=9, color='maroon', rotation=90)

    ax1.set_xticks([i + 0.2 for i in x])
    ax1.set_xticklabels(df['Label'], rotation=45, ha='right')
    ax1.set_ylabel("NPS Score")
    ax2.set_ylabel("No. of Responses")
    ax1.set_ylim(-100, 110)  # Adjust based on your data
    ax2.set_ylim(0, df['Responses'].max() + 10)

    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)
    ax1.set_title("ML Region Categories - NPS Evaluation")

    st.pyplot(fig)
else:
    st.info("📥 Please upload a CSV file in the required format.")
