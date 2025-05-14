import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import time

# Streamlit app title
st.title("3D Scatter Plot and Cause Distribution Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# Load or generate data
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    required_columns = {
        'properties.loc_x', 'properties.loc_y', 'properties.loc_z',
        'properties.cause', 'properties.carriage_id', 'properties.server_id'
    }
    if not required_columns.issubset(data.columns):
        st.error("CSV must contain columns: loc_x, loc_y, loc_z, cause, carriage_id, server_id")
        st.stop()
    st.success("CSV loaded successfully!")
else:
    # Generate test data
    np.random.seed(42)
    n = 100
    data = pd.DataFrame({
        'properties.loc_x': np.random.rand(n) * 10,
        'properties.loc_y': np.random.rand(n) * 10,
        'properties.loc_z': np.random.rand(n) * 10,
        'properties.cause': np.random.choice(['A', 'B', 'C'], n),
        'properties.carriage_id': np.random.choice(['Car1', 'Car2', 'Car3'], n),
        'properties.server_id': np.random.choice(['server1', 'server2', 'server3'], n)
    })

# Sidebar filters
st.sidebar.header("Filters")

# Cause filter
cause_options = ['All'] + sorted(data['properties.cause'].unique())
selected_cause = st.sidebar.selectbox("Select Cause", cause_options)

# Carriage ID filter
carriage_options = ['All'] + sorted(data['properties.carriage_id'].unique())
selected_carriage = st.sidebar.selectbox("Select Carriage ID", carriage_options)

# Server filter
server_options = ['All'] + sorted(data['properties.server_id'].unique())
selected_server = st.sidebar.selectbox("Select Server", server_options)

# Apply filters
filtered_data = data.copy()
if selected_cause != 'All':
    filtered_data = filtered_data[filtered_data['properties.cause'] == selected_cause]
if selected_carriage != 'All':
    filtered_data = filtered_data[filtered_data['properties.carriage_id'] == selected_carriage]
if selected_server != 'All':
    filtered_data = filtered_data[filtered_data['properties.server_id'] == selected_server]

# 3D Scatter Plot
fig_static = px.scatter_3d(
    filtered_data.copy(),
    x='properties.loc_x', y='properties.loc_y', z='properties.loc_z',
    color='properties.cause',
    title='3D Scatter Plot (Filtered)',
    labels={
        'properties.loc_x': 'X',
        'properties.loc_y': 'Y',
        'properties.loc_z': 'Z',
        'properties.cause': 'Cause'
    }
)

# Display scatter plot
st.plotly_chart(fig_static, use_container_width=True)

# Pie Chart of Cause Distribution
cause_counts = filtered_data['properties.cause'].value_counts().reset_index()
cause_counts.columns = ['Cause', 'Count']

fig_pie = px.pie(
    cause_counts.copy(),
    names='Cause',
    values='Count',
    title='Distribution of Causes',
    hole=0.3
)

# Display pie chart
st.plotly_chart(fig_pie, use_container_width=True)
