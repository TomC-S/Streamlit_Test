import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import time

# Streamlit app title
st.title("Shop Data")

# Upload CSV
uploaded_file = st.file_uploader("Choose a Mixpanel CSV file", type="csv")

if uploaded_file:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Convert time if exists
    if 'time' in df.columns:
        df['datetime'] = pd.to_datetime(df['time'], unit='ms')

    # Define target blueprint items
    weapon_items = [
        "Exchange.Blueprint.Weapon.Rifle_T2_AlphaStrike_Teal",
        "Exchange.Blueprint.Weapon.Rifle_T2_AlphaStrike_Red",
        "Exchange.Blueprint.Weapon.Rifle_T2_AlphaStrike_Blue"
    ]
    cosmetic_items = [
        "Exchange.Blueprint.Clothing.ScrapPunk.Boots",
        "Exchange.Blueprint.Clothing.ScrapPunk.Gloves",
        "Exchange.Blueprint.Clothing.ScrapPunk.Jacket",
        "Exchange.Blueprint.Clothing.ScrapPunk.Pants",
        "Exchange.Blueprint.Clothing.ScrapPunk.Singlet",
        "Exchange.Blueprint.Clothing.ScrapPunk.Headband",
        "Exchange.Blueprint.Armor.GasMask_T3_ToxicSkin",
        "Exchange.Blueprint.Armor.GasMask_T3_ToxicRedSkin",
        "Exchange.Blueprint.Armor.GasMask_T3_ToxicSkin_Spiky",
        "Exchange.Blueprint.Armor.GasMask_T3_ToxicZombieSkin"
    ]
    base_items = [
        "Exchange.Blueprint.Buildable.RecordPlayer",
    ]
    # Get columns for knowledge granted
    knowledge_columns = [col for col in df.columns if col.startswith("properties.knowledge_granted.")]

    # Count occurrences
    counts = {}
    for item in weapon_items:
        counts[item] = (df[knowledge_columns] == item).sum().sum()

    # Convert to DataFrame
    counts_df = pd.DataFrame(list(counts.items()), columns=["Blueprint", "Count"])

    cosmetic_counts = {}
    for item in cosmetic_items:
        cosmetic_counts[item] = (df[knowledge_columns] == item).sum().sum()

    # Convert to DataFrame
    cosmetic_counts_df = pd.DataFrame(list(cosmetic_counts.items()), columns=["Blueprint", "Count"])

    base_counts = {}
    for item in base_items:
        base_counts[item] = (df[knowledge_columns] == item).sum().sum()

    # Convert to DataFrame
    base_count_df = pd.DataFrame(list(base_counts.items()), columns=["Blueprint", "Count"])

    # Display table
    st.subheader("Weapon Counts")
    st.dataframe(counts_df)

   # Display bar chart with Plotly
    st.subheader("Weapons")
    fig = px.bar(
        counts_df,
        x="Blueprint",
        y="Count",
        title="Weapon Counts",
        labels={"Blueprint": "Blueprint", "Count": "Acquisitions"},
        text_auto=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

    st.subheader("Cosmetics")
    fig = px.bar(
        cosmetic_counts_df,
        x="Blueprint",
        y="Count",
        title="Cosmetic Counts",
        labels={"Blueprint": "Blueprint", "Count": "Acquisitions"},
        text_auto=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

    st.subheader("Base")
    fig = px.bar(
        base_count_df,
        x="Blueprint",
        y="Count",
        title="Cosmetic Counts",
        labels={"Blueprint": "Blueprint", "Count": "Acquisitions"},
        text_auto=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

    st.header("Battle Pass")