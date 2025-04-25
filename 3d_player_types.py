import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler

st.title("🎮 Player Event Metric Visualizer (3D Scatter + Clustering)")

uploaded_file = st.file_uploader("Upload CSV with columns: key.0 (distinct_id), key.1 (event_type), value", type="csv")

if uploaded_file:
    # Read and rename columns
    df = pd.read_csv(uploaded_file)
    df.columns = ['distinct_id', 'event_type', 'count']

    # Pivot to player-level feature matrix
    pivot_df = df.pivot_table(
        index='distinct_id',
        columns='event_type',
        values='count',
        fill_value=0
    ).reset_index()

    # Ensure required event types are present
    for col in ["syncs_extracted", "weapon_used", "building_placed"]:
        if col not in pivot_df.columns:
            pivot_df[col] = 0

    st.markdown("### 📋 Preview of Aggregated Player Metrics")
    st.dataframe(pivot_df, use_container_width=True)

    # ================================
    # 🔄 Shared Features + Scaling
    # ================================
    features = pivot_df[["weapon_used", "syncs_extracted", "building_placed"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # ================================
    # 🚀 KMeans Clustering
    # ================================
    st.subheader("📌 KMeans Clustering")
    num_clusters = st.slider("🔢 Number of KMeans Clusters", min_value=2, max_value=10, value=4)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    pivot_df["kmeans_cluster"] = kmeans.fit_predict(X_scaled)

    # --- 3D Plot for KMeans
    fig_kmeans = go.Figure(data=[go.Scatter3d(
        x=pivot_df["weapon_used"],
        y=pivot_df["syncs_extracted"],
        z=pivot_df["building_placed"],
        mode='markers',
        marker=dict(
            size=6,
            color=pivot_df["kmeans_cluster"],
            colorscale='Viridis',
            opacity=0.9,
            colorbar=dict(title="KMeans Cluster")
        ),
        text=pivot_df["distinct_id"],
        hovertemplate='<b>%{text}</b><br>weapon_used: %{x}<br>syncs_extracted: %{y}<br>building_placed: %{z}<br>KMeans Cluster: %{marker.color}<extra></extra>'
    )])

    fig_kmeans.update_layout(
        scene=dict(
            xaxis_title='weapon_used',
            yaxis_title='syncs_extracted',
            zaxis_title='building_placed',
        ),
        title="🔍 KMeans Clustered Player Activity Map (3D)",
        margin=dict(l=0, r=0, b=0, t=30)
    )

    st.plotly_chart(fig_kmeans, use_container_width=True)

    # --- KMeans Cluster Summary
    st.markdown("### 📊 KMeans Cluster Summary")
    kmeans_summary = pivot_df.groupby("kmeans_cluster").agg(
        Players=("distinct_id", "count"),
        Avg_Weapon_Used=("weapon_used", "mean"),
        Avg_Syncs_Extracted=("syncs_extracted", "mean"),
        Avg_Building_Placed=("building_placed", "mean")
    ).reset_index()

    st.dataframe(kmeans_summary)

    # ================================
    # 🔍 DBSCAN Clustering (Separate Graph)
    # ================================
    st.subheader("📌 DBSCAN Clustering")

    st.sidebar.markdown("### ⚙️ DBSCAN Parameters")
    eps = st.sidebar.slider("DBSCAN eps (neighborhood size)", min_value=0.1, max_value=5.0, value=1.2, step=0.1)
    min_samples = st.sidebar.slider("DBSCAN min_samples", min_value=1, max_value=10, value=5, step=1)

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    pivot_df["dbscan_cluster"] = dbscan.fit_predict(X_scaled)

    # --- 3D Plot for DBSCAN
    fig_dbscan = go.Figure(data=[go.Scatter3d(
        x=pivot_df["weapon_used"],
        y=pivot_df["syncs_extracted"],
        z=pivot_df["building_placed"],
        mode='markers',
        marker=dict(
            size=6,
            color=pivot_df["dbscan_cluster"],
            colorscale='Plasma',
            opacity=0.9,
            colorbar=dict(title="DBSCAN Cluster")
        ),
        text=pivot_df["distinct_id"],
        hovertemplate='<b>%{text}</b><br>weapon_used: %{x}<br>syncs_extracted: %{y}<br>building_placed: %{z}<br>DBSCAN Cluster: %{marker.color}<extra></extra>'
    )])

    fig_dbscan.update_layout(
        scene=dict(
            xaxis_title='weapon_used',
            yaxis_title='syncs_extracted',
            zaxis_title='building_placed',
        ),
        title="🧬 DBSCAN Clustered Player Activity Map (3D)",
        margin=dict(l=0, r=0, b=0, t=30)
    )

    st.plotly_chart(fig_dbscan, use_container_width=True)

    # --- DBSCAN Cluster Summary
    st.markdown("### 📊 DBSCAN Cluster Summary (includes noise: -1)")
    dbscan_summary = pivot_df.groupby("dbscan_cluster").agg(
        Players=("distinct_id", "count"),
        Avg_Weapon_Used=("weapon_used", "mean"),
        Avg_Syncs_Extracted=("syncs_extracted", "mean"),
        Avg_Building_Placed=("building_placed", "mean")
    ).reset_index()

    st.dataframe(dbscan_summary)

