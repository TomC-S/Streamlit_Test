import streamlit as st
import plotly.graph_objects as go
import numpy as np


st.title('Hello, Streamlit!')
st.write('This is my first Streamlit app.')


# Generate test data
np.random.seed(42)
n = 50  # Number of points
x = np.random.rand(n) * 10
y = np.random.rand(n) * 10
z = np.random.rand(n) * 10

# Create 3D scatter plot
fig = go.Figure(data=[go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(size=6, color=z, colorscale='Viridis', opacity=0.8)
)])

# Layout adjustments
fig.update_layout(
    title='3D Scatter Plot',
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Streamlit app
st.title("3D Scatter Plot Example")
st.plotly_chart(fig)