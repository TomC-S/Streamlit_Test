import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Shop Data")

# Upload CSV
uploaded_file = st.file_uploader("Choose a Mixpanel CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'time' in df.columns:
        df['datetime'] = pd.to_datetime(df['time'], unit='ms')

    # Define blueprint groups
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
    bp_page_1 = [
        "Exchange.Blueprint.Clothing.Rocker.TShirt",
        "Exchange.Blueprint.Clothing.Rocker.Gloves",
        "Exchange.Blueprint.Clothing.Rocker.Boots",
        "Exchange.Blueprint.Armor.GasMask_T3_SkullSkin",
        "Exchange.KnowledgeLoadout.ResourceKit",
        "Exchange.Blueprint.Armor.Perks.Gunner",
        "Exchange.Blueprint.Armor.Perks.Raider",
        "Exchange.Blueprint.Weapon.RifleT2Reskin",
    ]
    bp_page_2 = [
        "Exchange.Blueprint.Clothing.Rocker.Headphones",
        "Exchange.Blueprint.Clothing.Rocker.Headband",
        "Exchange.Blueprint.Clothing.Rocker.Mask",
        "Exchange.Blueprint.Clothing.Rocker.Pants",
        "Exchange.KnowledgeLoadout.BaseInABox",
        "Exchange.Blueprint.Armor.Perks.Craftsman",
        "Exchange.Blueprint.Armor.Perks.Rogue",
        "Exchange.Blueprint.Buildable.bedroll_Reskin"
    ]
    bp_page_3 = [
        "Exchange.KnowledgeLoadout.PlasticSMG",
        "Exchange.Blueprint.Clothing.Rocker.Jacket",
        "Exchange.KnowledgeLoadout.ImprovShotgun",
        "Exchange.Blueprint.Weapon.Rifle_T3_Reskin",
    ]

    # Get knowledge columns and melt to long format
    knowledge_columns = [col for col in df.columns if col.startswith("properties.knowledge_granted.")]
    melted_df = df.melt(id_vars=["distinct_id"], value_vars=knowledge_columns, value_name="Blueprint").dropna()
    unique_grants = melted_df.drop_duplicates(subset=["distinct_id", "Blueprint"])

    # Generic function to count distinct_id per blueprint
    def count_group(group_items):
        filtered = unique_grants[unique_grants["Blueprint"].isin(group_items)]
        return (
            filtered.groupby("Blueprint")["distinct_id"]
            .nunique()
            .reset_index()
            .rename(columns={"distinct_id": "Count"})
        )

    # Create and plot each section
    def show_chart(title, items):
        data = count_group(items)
        st.subheader(title)
        st.dataframe(data)
        fig = px.bar(
            data,
            x="Blueprint",
            y="Count",
            title=title,
            labels={"Blueprint": "Blueprint", "Count": "Unique Players"},
            text_auto=True
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

    # Render each section
    show_chart("Weapon Counts", weapon_items)
    show_chart("Cosmetic Counts", cosmetic_items)
    show_chart("Base Counts", base_items)

    # Combine all shop items
    shop_items = weapon_items + cosmetic_items + base_items

    # Get players who received any shop item
    shop_spenders = unique_grants[unique_grants["Blueprint"].isin(shop_items)]["distinct_id"].unique()

    # Display total shop spenders
    st.header("Shop Spend Summary")
    st.markdown(f"**Total players who acquired at least one item from the shop: {len(shop_spenders)}**")

    st.markdown("**Player IDs:**")
    st.write(shop_spenders.tolist())

    # Battle Pass Section
    st.header("Battle Pass")

    def count_bp_page(items, page_name):
        df_page = count_group(items)
        df_page["Page"] = page_name
        return df_page

    bp1_df = count_bp_page(bp_page_1, "Page 1")
    bp2_df = count_bp_page(bp_page_2, "Page 2")
    bp3_df = count_bp_page(bp_page_3, "Page 3")
    bp_df = pd.concat([bp1_df, bp2_df, bp3_df], ignore_index=True)

    for page, items in [("Page 1", bp_page_1), ("Page 2", bp_page_2), ("Page 3", bp_page_3)]:
        # Filter and count unique acquisitions
        page_df = count_group(items)
        page_df["Page"] = page

        # Plot
        st.subheader(f"Battle Pass {page}")
        fig = px.bar(
            page_df,
            x="Blueprint",
            y="Count",
            title=f"Battle Pass {page} - Unique Player Acquisitions",
            labels={"Blueprint": "Blueprint", "Count": "Unique Players"},
            text_auto=True
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

          # Get players who have all the blueprints on this page
        all_items_df = (
            unique_grants[unique_grants["Blueprint"].isin(items)]
            .groupby("distinct_id")["Blueprint"]
            .nunique()
            .reset_index()
        )
        full_owners = all_items_df[all_items_df["Blueprint"] == len(items)]["distinct_id"]

        # Display count and IDs
        st.markdown(f"**Players who acquired all {len(items)} rewards on {page}: {len(full_owners)}**")
        st.markdown("**Player IDs:**")
        st.write(full_owners.tolist())
