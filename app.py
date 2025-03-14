import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

st.title('Test McTest!')
st.write('Deaths in Carriage')

st.write('Drop CSV here and use the filter to see different causes of death')

# CSV Upload Option
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if {'loc_x', 'loc_y', 'loc_z', 'cause'}.issubset(data.columns):
        st.success("CSV loaded successfully!")
    else:
        st.error("CSV must contain columns:loc_x, loc_y, loc_z, and cause")
        st.stop()
else:
    # Generate test data if no file is uploaded
    np.random.seed(42)
    n = 50  # Number of points
    data = pd.DataFrame({
        'loc_x': np.random.rand(n) * 10,
        'loc_y': np.random.rand(n) * 10,
        'loc_z': np.random.rand(n) * 10,
        'cause': np.random.choice(['A', 'B', 'C'], n)  # Random categories
    })

# Streamlit selector for filtering cause
cause_options = ['All'] + sorted(data['cause'].unique().tolist())
selected_cause = st.selectbox("Select Cause to Display", cause_options)

# Filter data based on selection
if selected_cause != 'All':
    filtered_data = data[data['cause'] == selected_cause]
else:
    filtered_data = data

# Create 3D scatter plot using plotly express
fig = px.scatter_3d(
    filtered_data, x='loc_x', y='loc_y', z='loc_z',
    color='cause',  # Different colors for different causes
    size_max=6,
    title='3D Scatter Plot',
    labels={'x': 'X Axis', 'y': 'Y Axis', 'z': 'Z Axis', 'cause': 'Cause'}
)

st.plotly_chart(fig)
