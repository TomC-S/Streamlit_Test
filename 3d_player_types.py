import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.title("🎮 Player Event Metric Visualizer (3D Scatter + Clustering)")

uploaded_file = st.file_uploader("Upload CSV with columns: key.0 (distinct_id), key.1 (event_type), value", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = ['distinct_id', 'event_type', 'count']

    pivot_df = df.pivot_table(
        index='distinct_id',
        columns='event_type',
        values='count',
        fill_value=0
    ).reset_index()

    for col in ["syncs_extracted", "weapon_used", "building_placed"]:
        if col not in pivot_df.columns:
            pivot_df[col] = 0

    st.markdown("### 📋 Preview of Aggregated Player Metrics")
    st.dataframe(pivot_df, use_container_width=True)

    # ================================
    # 🚀 KMeans Clustering
    # ================================
    features = pivot_df[["weapon_used", "syncs_extracted", "building_placed"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Select number of clusters
    num_clusters = st.slider("🔢 Number of Clusters", min_value=2, max_value=10, value=4)

    # Run KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    pivot_df["cluster"] = kmeans.fit_predict(X_scaled)

    # ================================
    # 🎯 3D Plot with Clustering Colors
    # ================================
    fig = go.Figure(data=[go.Scatter3d(
        x=pivot_df["weapon_used"],
        y=pivot_df["syncs_extracted"],
        z=pivot_df["building_placed"],
        mode='markers',
        marker=dict(
            size=6,
            color=pivot_df["cluster"],  # 🧠 color by cluster
            colorscale='Viridis',
            opacity=0.9,
            colorbar=dict(title="Cluster")
        ),
        text=pivot_df["distinct_id"],
        hovertemplate='<b>%{text}</b><br>weapon_used: %{x}<br>syncs_extracted: %{y}<br>building_placed: %{z}<br>Cluster: %{marker.color}<extra></extra>'
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title='weapon_used',
            yaxis_title='syncs_extracted',
            zaxis_title='building_placed',
        ),
        title="🔍 Clustered Player Activity Map (3D)",
        margin=dict(l=0, r=0, b=0, t=30)
    )

    st.plotly_chart(fig, use_container_width=True)
