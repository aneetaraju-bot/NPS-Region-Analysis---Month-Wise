import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 ML Region Categories - NPS Evaluation")

# Load CSV
df = pd.read_csv("data/nps_july.csv")

# Fill missing values
df[['Vertical', 'Region']] = df[['Vertical', 'Region']].fillna(method='ffill')

# Select required columns
df = df[['Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No: of Responses']]
df.columns = ['Vertical', 'Region', 'Status', 'NPS_Score', 'Responses']
df.dropna(subset=['NPS_Score', 'Responses'], inplace=True)

# Convert to numbers
df['NPS_Score'] = pd.to_numeric(df['NPS_Score'], errors='coerce')
df['Responses'] = pd.to_numeric(df['Responses'], errors='coerce')

# Dropdown for region
regions = df['Region'].dropna().unique()
selected_region = st.selectbox("Select Region", options=sorted(regions))

# Filter and create label
filtered_df = df[df['Region'] == selected_region].copy()
filtered_df['Label'] = filtered_df['Vertical'] + " - " + filtered_df['Status']
filtered_df.sort_values(by='Vertical', inplace=True)

# Plot
fig, ax1 = plt.subplots(figsize=(16, 6))
x = range(len(filtered_df))

ax1.bar(x, filtered_df['NPS_Score'], width=0.4, label='NPS Score', color='cornflowerblue')
ax2 = ax1.twinx()
ax2.bar([i + 0.4 for i in x], filtered_df['Responses'], width=0.4, label='Responses', color='seagreen')

ax1.set_xticks([i + 0.2 for i in x])
ax1.set_xticklabels(filtered_df['Label'], rotation=45, ha='right')
ax1.set_ylabel("NPS Score")
ax2.set_ylabel("No. of Responses")
ax1.set_title(f"NPS Evaluation - {selected_region}")
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

st.pyplot(fig)
