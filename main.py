import streamlit as st
import pandas as pd

# Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1CWYqKdx3MQP1eRqU1Bb4nBNh5frm1a4KX_FV8-xN9T0/edit?usp=sharing"
csv_export_url = sheet_url.replace('/edit?usp=sharing', '/export?format=csv')

# Load data from Google Sheets
data = pd.read_csv(csv_export_url)

# Display the first few rows of the DataFrame

st.title("Urban Heat Island Effect Mitigation Strategies")
st.write("Our platform aims to provide a comprehensive overview of the Urban Heat Island Effect and the various strategies that can be implemented to mitigate it. The data presented here is collect through crowdsourcing and is open to contributions from the public in India & Pakistan. If you have any information that you would like to share, please feel free to reach out to us.")
st.write(data.head())
st.write(data.columns)
