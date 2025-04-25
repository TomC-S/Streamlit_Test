import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🎮 Player Event Metric Visualizer (3D Scatter)")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV with columns: key.0 (distinct_id), key.1 (event_type), value", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Rename columns for clarity based on actual structure
    df.columns = ['distinct_id', 'event_type', 'count']

    # Pivot the data: one row per distinct_id, one column per event type
    pivot_df = df.pivot_table(
        index='distinct_id',
        columns='event_type',
        values='count',
        fill_value=0
    ).reset_index()

    # Ensure all 3 event columns exist, even if missing in the data
    for col in ["syncs_extracted", "weapon_used", "building_placed"]:
        if col not in pivot_df.columns:
            pivot_df[col] = 0

    st.markdown("### 📋 Preview of Aggregated Player Metrics")
    st.dataframe(pivot_df, use_container_width=True)

    # Create 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=pivot_df["weapon_used"],
        y=pivot_df["syncs_extracted"],
        z=pivot_df["building_placed"],
        mode='markers',
        marker=dict(
            size=5,
            color=pivot_df["building_placed"],
            colorscale='Viridis',
            opacity=0.8
        ),
        text=pivot_df["distinct_id"],
        hovertemplate='<b>%{text}</b><br>weapon_used: %{x}<br>syncs_extracted: %{y}<br>building_placed: %{z}<extra></extra>'
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title='weapon_used',
            yaxis_title='syncs_extracted',
            zaxis_title='building_placed',
        ),
        title="🧠 3D Player Event Activity Map",
        margin=dict(l=0, r=0, b=0, t=30)
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 Upload a Mixpanel-exported CSV to get started.")
