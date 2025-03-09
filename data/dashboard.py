import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
def load_data():
    file_path = '../data/data_1.csv'
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.set_index('datetime', inplace=True)
    df['PM2.5'].fillna(df['PM2.5'].median(), inplace=True)
    df['hour'] = df.index.hour
    return df

df = load_data()

# Dashboard Title
st.title("Proyek Analisis Data: [Air-Quality-Dataset]")

# Sidebar Filters
st.sidebar.header("Filters")
view = st.sidebar.selectbox("Select View", ["Overview", "Seasonal Patterns", "Wind Speed Relationship"])

# Overview
if view == "Overview":
    st.header("Dataset Overview")
    st.dataframe(df.head())
    st.subheader("Statistics")
    st.write(df.describe())

    # PM2.5 Distribution
    st.subheader("PM2.5 Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['PM2.5'], bins=30, kde=True, color='skyblue', ax=ax)
    ax.set_title('Distribution of PM2.5')
    st.pyplot(fig)

# Seasonal Patterns
elif view == "Seasonal Patterns":
    st.header("Seasonal Patterns of PM2.5")
    # Monthly Trend
    monthly_avg = df.resample('M')['PM2.5'].mean()
    fig, ax = plt.subplots()
    monthly_avg.plot(ax=ax)
    ax.set_title('Monthly Average PM2.5 Concentration')
    st.pyplot(fig)

    # Hourly Trend
    hourly_avg = df.groupby('hour')['PM2.5'].mean()
    fig, ax = plt.subplots()
    hourly_avg.plot(ax=ax)
    ax.set_title('Hourly Average PM2.5 Concentration')
    st.pyplot(fig)

# Wind Speed Relationship
elif view == "Wind Speed Relationship":
    st.header("Relationship Between Wind Speed and PM2.5")
    fig, ax = plt.subplots()
    sns.scatterplot(x='WSPM', y='PM2.5', data=df, color='purple', ax=ax)
    ax.set_title('Wind Speed vs PM2.5')
    st.pyplot(fig)

    # Correlation Heatmap
    corr = df[['PM2.5', 'WSPM']].corr()
    st.subheader("Correlation")
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# Run Streamlit App Instruction
st.sidebar.markdown("### How to run this app:")
st.sidebar.code("streamlit run dashboard.py")