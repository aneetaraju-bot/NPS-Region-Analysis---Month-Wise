import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 ML Region Categories - NPS Evaluation")

# Upload file
uploaded_file = st.file_uploader("Upload your NPS CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV
    df = pd.read_csv(uploaded_file)

    # Fill missing Vertical and Region
    df[['Vertical', 'Region']] = df[['Vertical', 'Region']].fillna(method='ffill')

    # Select required columns
    try:
        df = df[['Vertical', 'Region', 'Status', 'NPS Score %', 'SUM of No]()]()
