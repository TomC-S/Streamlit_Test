import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

st.title('Hello, Streamlit!')
st.write('Kill in Carriage')

# Generate test data
np.random.seed(42)
n = 50  # Number of points
data = pd.DataFrame({
    'x': np.random.rand(n) * 10,
    'y': np.random.rand(n) * 10,
    'z': np.random.rand(n) * 10
})

# Create 3D scatter plot using plotly express
fig = px.scatter_3d(
    data, x='x', y='y', z='z',
    color='z', size_max=6,
    title='3D Scatter Plot',
    labels={'x': 'X Axis', 'y': 'Y Axis', 'z': 'Z Axis'}
)

# Streamlit app
st.title("3D Scatter Plot Example")
st.plotly_chart(fig)
