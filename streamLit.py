import streamlit as st
import pandas as pd
from google.cloud import bigquery
import plotly.express as px

# Set up BigQuery client
@st.cache_data
def load_data_from_bigquery():
    client = bigquery.Client.from_service_account_json("/Users/spartan/Downloads/SEM-2_Assignments/255-Data-Mining/assignment_1/bigquery-key.json")  # Use JSON key file
    query = """
    SELECT 
        LATITUDE, 
        LONGITUDE, 
        CRASHDATETIME, 
        PRIMARYCOLLISIONFACTOR, 
        INJURYSEVERITY, 
        YEAR, 
        VEHICLECOUNT, 
        HOUR,
        DAYOFWEEKNAME,
        MONTHNAME,
        SEVERITY_CATEGORY
    FROM `cloud-data-mining-452501.processed_data.cleaned_crash_data`
    """
    df = client.query(query).to_dataframe()
    return df


# Load data
st.title("Crash Data Analysis Dashboard")
st.write("This dashboard visualizes crash data interactively.")
df = load_data_from_bigquery()

# Sidebar Filters
st.sidebar.header("Filters")
selected_year = st.sidebar.multiselect("Select Year(s):", options=df['YEAR'].unique(), default=df['YEAR'].unique())
selected_cause = st.sidebar.multiselect("Select Crash Cause(s):", options=df['PRIMARYCOLLISIONFACTOR'].unique(), default=df['PRIMARYCOLLISIONFACTOR'].unique())
selected_severity = st.sidebar.multiselect("Select Severity Level(s):", options=df['SEVERITY_CATEGORY'].unique(), default=df['SEVERITY_CATEGORY'].unique())

# Filter data based on selections
filtered_data = df[
    (df['YEAR'].isin(selected_year)) &
    (df['PRIMARYCOLLISIONFACTOR'].isin(selected_cause)) &
    (df['SEVERITY_CATEGORY'].isin(selected_severity))
]

# Section 1: Line Chart - Crashes Over Time
st.subheader("Number of Crashes Over Time")
line_chart_data = filtered_data.groupby('YEAR').size().reset_index(name='total_crashes')
fig_line = px.line(line_chart_data, x='YEAR', y='total_crashes', title="Crashes Over Time", markers=True)
st.plotly_chart(fig_line)

# Section 2: Bar Chart - Top Causes of Crashes
st.subheader("Top Causes of Crashes")
cause_chart_data = filtered_data['PRIMARYCOLLISIONFACTOR'].value_counts().reset_index()
cause_chart_data.columns = ['Cause', 'Count']
fig_bar = px.bar(cause_chart_data, x='Count', y='Cause', orientation='h', title="Top Causes of Crashes")
st.plotly_chart(fig_bar)

# Section 3: Geo Map - Crash Locations
st.subheader("Crash Locations")
fig_map = px.scatter_mapbox(
    filtered_data,
    lat='LATITUDE',
    lon='LONGITUDE',
    color='SEVERITY_CATEGORY',
    size='VEHICLECOUNT',
    hover_name='PRIMARYCOLLISIONFACTOR',
    mapbox_style="open-street-map",
    title="Crash Locations"
)
st.plotly_chart(fig_map)

# Section 4: Pie Chart - Severity Distribution
st.subheader("Crash Severity Distribution")
severity_chart_data = filtered_data['SEVERITY_CATEGORY'].value_counts().reset_index()
severity_chart_data.columns = ['Severity', 'Count']
fig_pie = px.pie(severity_chart_data, names='Severity', values='Count', title="Severity Distribution")
st.plotly_chart(fig_pie)

