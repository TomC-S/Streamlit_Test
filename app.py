import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import time

# Streamlit app
st.title("3D Scatter Plot Example")

# CSV Upload Option
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if {'loc_x', 'loc_y', 'loc_z', 'cause', 'carriage_id', 'time'}.issubset(data.columns):
        st.success("CSV loaded successfully!")
        # Convert Unix time to datetime format and round to the nearest minute
        data['time'] = pd.to_datetime(data['time'], unit='s').dt.floor('min')
    else:
        st.error("CSV must contain columns: loc_x, loc_y, loc_z, cause, carriage_id, and time (Unix format)")
        st.stop()
else:
    # Generate test data if no file is uploaded
    np.random.seed(42)
    n = 100  # Number of points
    current_time = int(time.time())  # Current Unix timestamp
    data = pd.DataFrame({
        'loc_x': np.random.rand(n) * 10,
        'loc_y': np.random.rand(n) * 10,
        'loc_z': np.random.rand(n) * 10,
        'cause': np.random.choice(['A', 'B', 'C'], n),  # Random categories
        'carriage_id': np.random.choice(['Car1', 'Car2', 'Car3'], n),  # Random carriage IDs
        'time': np.random.randint(current_time, current_time + 3600, n)  # Random Unix timestamps in next hour
    })
    data['time'] = pd.to_datetime(data['time'], unit='s').dt.floor('min')  # Convert to datetime and round to minute

# Streamlit selector for filtering cause
cause_options = ['All'] + sorted(data['cause'].unique().tolist())
selected_cause = st.selectbox("Select Cause to Display", cause_options)

# Streamlit selector for filtering carriage_id
carriage_options = ['All'] + sorted(data['carriage_id'].unique().tolist())
selected_carriage = st.selectbox("Select Carriage ID to Display", carriage_options)

# Filter data based on selections
filtered_data = data
if selected_cause != 'All':
    filtered_data = filtered_data[filtered_data['cause'] == selected_cause]
if selected_carriage != 'All':
    filtered_data = filtered_data[filtered_data['carriage_id'] == selected_carriage]

# Ensure animation shows all kills up to the current time frame
filtered_data = filtered_data.sort_values(by='time')
cumulative_data = []
for t in filtered_data['time'].unique():
    subset = filtered_data[filtered_data['time'] <= t].copy()  # Apply filters to animated dataset as well
    subset['cumulative_time'] = t  # Assign same time for proper animation grouping
    cumulative_data.append(subset)
cumulative_data = pd.concat(cumulative_data)

# Static 3D Scatter Plot
fig_static = px.scatter_3d(
    filtered_data, x='loc_x', y='loc_y', z='loc_z',
    color='cause',  # Different colors for different causes
    size_max=6,
    title='3D Scatter Plot (Static)',
    labels={'loc_x': 'X Axis', 'loc_y': 'Y Axis', 'loc_z': 'Z Axis', 'cause': 'Cause', 'carriage_id': 'Carriage ID'}
)

# Animated 3D Scatter Plot with Time Scrub
fig_animated = px.scatter_3d(
    cumulative_data, x='loc_x', y='loc_y', z='loc_z',
    color='cause',  # Different colors for different causes
    size_max=6,
    title='3D Scatter Plot with Cumulative Time Animation',
    labels={'loc_x': 'X Axis', 'loc_y': 'Y Axis', 'loc_z': 'Z Axis', 'cause': 'Cause', 'carriage_id': 'Carriage ID', 'cumulative_time': 'Time'},
    animation_frame='cumulative_time'  # Animate showing all points up to each time frame
)

# Display both plots
st.plotly_chart(fig_static)
st.plotly_chart(fig_animated)

# ---- Building Placement Visualization ----

# CSV Upload Option for Buildings
uploaded_building_file = st.file_uploader("Upload Buildings CSV file", type=["csv"], key="buildings")
if uploaded_building_file is not None:
    df_buildings = pd.read_csv(uploaded_building_file)
    if {'properties.building_id', 'properties.loc_x', 'properties.loc_y', 'properties.loc_z', 'properties.carriage_id'}.issubset(df_buildings.columns):
        st.success("Buildings CSV loaded successfully!")
    else:
        st.error("Buildings CSV must contain columns: properties.building_id, properties.loc_x, properties.loc_y, properties.loc_z, and properties.carriage_id")
        st.stop()
else:
    df_buildings = None

if df_buildings is not None:
    st.title("3D Scatter Plot for Buildings")

    # Streamlit selector for filtering building_id
    building_id_options = ['All'] + sorted(df_buildings['properties.building_id'].unique().tolist())
    selected_building_id = st.selectbox("Select Building ID", building_id_options)
    
    # Streamlit selector for filtering building carriage_id
    building_carriage_options = ['All'] + sorted(df_buildings['properties.carriage_id'].unique().tolist())
    selected_building_carriage = st.selectbox("Select Carriage ID for Buildings", building_carriage_options)

    # Filter buildings data based on selections
    filtered_buildings = df_buildings
    if selected_building_id != 'All':
        filtered_buildings = filtered_buildings[filtered_buildings['properties.building_id'] == selected_building_id]
    if selected_building_carriage != 'All':
        filtered_buildings = filtered_buildings[filtered_buildings['properties.carriage_id'] == selected_building_carriage]

    # Static 3D Scatter Plot for Buildings
    fig_buildings = px.scatter_3d(
        filtered_buildings, x='properties.loc_x', y='properties.loc_y', z='properties.loc_z',
        color='properties.building_id',  # Different colors for different buildings
        size_max=6,
        title='3D Scatter Plot for Buildings',
        labels={'properties.loc_x': 'X Axis', 'properties.loc_y': 'Y Axis', 'properties.loc_z': 'Z Axis', 'properties.carriage_id': 'Carriage ID', 'properties.building_id': 'Building ID'}
    )

    # Display buildings plot
    st.plotly_chart(fig_buildings)
