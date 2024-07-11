'''
https://www.perplexity.ai/search/write-a-streamlit-app-that-dow-.4Bwqr1cS76dVyN4hgO1gg

write a streamlit app that downloads data from the ishares website 
for the emerging market bond index and then analyses the data
Sources

also this:
https://share.streamlit.io/streamlit/emoji-shortcodes

'''


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO
from datetime import date

st.set_page_config(
    page_title= 'iShares Analysis',
    page_icon=':mushroom:'
    )
st.title('iShares Emerging Market Bond Index Analysis')

# Download data from iShares website
@st.cache_data
def load_data():
    url = "https://www.ishares.com/us/products/239572/ishares-jp-morgan-usd-emerging-markets-bond-etf/1467271812596.ajax?fileType=csv&fileName=EMB_holdings&dataType=fund"
    response = requests.get(url)
    data = pd.read_csv(StringIO(response.text), skiprows=9)
    return data

data = load_data()

st.write("## Raw Data Head")
st.dataframe(data.head())

# Basic data analysis
st.write("## Data Analysis")

# Top 10 holdings by weight
st.write("### Top 10 Holdings by Weight")
top_10 = data.nlargest(10, 'Weight (%)')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Weight (%)', y='Name', data=top_10)
plt.title("Top 10 Holdings by Weight")
st.pyplot(fig)

# Distribution of maturities
st.write("### Distribution of Maturities")

# Get today's date
today = date.today()

# Convert the date column to datetime, setting invalid dates to NaT
data['Maturity'] = pd.to_datetime(
    data['Maturity'], format='%b %d, %Y', errors='coerce')
data['Maturity'] = data['Maturity'].fillna(today)
data['Maturity'] = pd.to_datetime(data['Maturity'], format='%b %d, %Y')
data['Years to Maturity'] = (
    pd.to_datetime(data['Maturity']).dt.year - pd.Timestamp.now().year)
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data['Years to Maturity'], bins=20, kde=True)
plt.title("Distribution of Years to Maturity")
plt.xlabel("Years to Maturity")
st.pyplot(fig)

# Coupon distribution
st.write("### Coupon Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data['Coupon (%)'], bins=20, kde=True)
plt.title("Distribution of Coupon Rates")
plt.xlabel("Coupon Rate (%)")
st.pyplot(fig)

# Country allocation
st.write("### Location Allocation")
country_allocation = data.groupby('Location')['Weight (%)'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 6))
country_allocation.plot(kind='pie', autopct='%1.1f%%', ax=ax)
plt.title("Top 10 Location by Weight")
st.pyplot(fig)

# Correlation matrix
st.write("### Correlation Matrix")
numeric_columns = ['Weight (%)', 'Price', 'Coupon (%)', 'Years to Maturity']
correlation_matrix = data[numeric_columns].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
plt.title("Correlation Matrix of Numeric Variables")
st.pyplot(fig)


st.write("## All Data")
st.dataframe(data)
