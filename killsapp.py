import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx

st.header("🤔 Player Kills Network Graph")

# Upload interaction data
uploaded_interaction_file = st.file_uploader("Upload Player Interaction CSV", type=["csv"], key="interactions")
if uploaded_interaction_file:
    df_interaction = pd.read_csv(uploaded_interaction_file)
else:
    st.warning("Please upload an interaction CSV file to proceed.")
    st.stop()

# Check required columns
required_cols = {'distinct_id', 'target_player_id', 'server_id', 'item_id'}
if required_cols.issubset(df_interaction.columns):

    # 🧠 Hardcoded Mixpanel ID → Name mapping
    mixpanel_lookup = {
        "24fe09008d0b1af05fc581fb7c0bc202": "Tnnr",
        "53f59f690061322b8190205acded4335": "Tom C-S",
        "35ca36db59eda90f585a933b16769d48": "Chris",
        "07395c25628d1690ea53211e5f7d34d4": "Joe",
        "c7542ba263bcff7cda1d07b2436a69ec": "Aiden",
        "0e6b7895a9ab8de6cd2fed46ed0736b4": "Rick",
        "50a61c8ab264485bfee3dcd52525ce78": "Marek",
        "48daccf783865184ea79fbffabf1aa2a": "Flak",
        "977bd157c12c355f8755fb9dd4141d89": "Kelton",
        "22ee8370fc3b7bc30a1854149a85adc2": "Caramel",
        "3953f45ca46458706f7b683c11d42cf3": "Skullsen",
        "e479b062d73ec02381928416a47488da": "Justin",
        "df8aa1903f1853773e464eaca2ce09c3": "Scooper",
        "070006813ea0cb5371edbd7f37647fd8": "Karma/Seb",
        "b623c05795703ef2244bf928257b6a22": "Simon",
        "eac8abd0e1fd766aeb51e152a01c667d": "Fred",
        "920b23260de934782ac5c13a276f74ef": "Bolton",
        "0b6bf12a8ee6c34098c1ad7b96e1ffd7": "Lukáš",
        "e90651401bc36200949531b45fbcaff3": "Taylor",
        "63ddcc10110aec0cc95c17ca7f71372c": "Nathan",
        "b9d4837fe1e9d19a96621849e489647b": "Dhiksha",
        "1ec91b702c556810600fda99fa3e3f14": "JAKSON",
        "b450207428ea58c7d5ef76d8eac16e45": "Jack northwave",
        "5273d32335bd34f880f68feafd2b5def": "Jane",
        "fa81ed628753307bb5a0c14d1e09a686": "Pola",
        "fd027eeca9f7bf8edf06d0ff0ebab26b": "Ethan",
        "3dcad7d80ababda0fa80f08ebdeb3b1d": "Ben Dover",
        "d16f8351b5c2b18286a7f37602a1fb3e": "Mr. Night",
        "8a0c068c59642a119071d65952e2ee0e": "Laura",
        "b2bb1e5bbfa23968041eb6b6ce6701ae": "Eivind",
        "e01821b7c589094530877297c0f4e2e1": "david",
        "627a8aebeeeea0310c8c7ca7aab7a24e": "Andreas",
        "09841e1bd615e19f86591143609056db": "Katerina",
        "01a23454d9f6acb6f85d82a6a599de63": "Bubbles",
        "7713dc5301bce3d768b04f9faf9696d7": "Rachel",
        "c8b00a89b47b4f921503210d84cf9ce5": "conor",
        "0275cb4b548910bb7d94f0f921867e41": "selina",
        "041d69adfe237190723db1eb3131868e": "Tableflip",
        "0b170ac773842f0f31a9b330a583bcc2": "ThePsydeFX",
        "0fb0918a28880c23b12a0f2b93d5e570": "bryn",
        "18ec936b288ff76a88ed605bd640ac34": "RoBoHoBo",
        "1ae65e32ac9bf53ec89a19010ab41a20": "Uberkist3",
        "2690c6010367c621ad9baecf483c2054": "ayessha",
        "5060239ec0b417a4327b3fdd5f1d4aa4": "kjetil",
        "51e7d925a58eadba70c96dfb90d1f070": "wardy",
        "6eeb7b6cf8d95352695837b4a41bd634": "luca",
        "8531aaa75686d2d91e02f97e942801d9": "adam",
        "8b0409bfa68b990054d00493ee9d9a4d": "Trade surplus",
        "94039c69b9fada91fdeacfd29d582ada": "rich",
        "971e22147daee533ef799dc4900798fe": "Oggli",
        "b5bfec92e4907bbe3a9283e83410318a": "Helix Crowley",
        "c21eec38cac93c735cc482116be13da7": "Fuszherbaty",
        "c8907e71ed45692963abf1108443fa89z": "kaya",
        "d4b8181aeafa956755ed9a059ecd591d": "Da Donk",
        "d6e17fe1ad36353253e3ae0a3ae5464d": "Jeeb",
        "deddd35089e6403500185b84489ef5c1": "mariana",
        "ef0f36e78e29a0f8b93eccee64f54dc1": "pokerplate",
        "f46b68022238154d3d62a76fcb6e35e8": "Dan G",
        "f5be2eeb2a817351a3d2dec564e3d17d": "shady",
        "06780e895099cb806c80a567f75db5df": "Michael Kaiser",
        "0bf4abd679c79c7e5373cb5f20b18181": "Chris B",
        "1750bd9e52a054cc61884eabb4747031": "Vernillet",
        "51f030a8b174949065cc55d04a5459e3": "Wade",
        "56982435fc9c5c78228a93c0b85a287d": "Kilinit",
        "5a5fbe9fd10cd3c43e8cc1b444b6f7be": "Gusgus",
        "5c9f4582c6c7f570a3b4affa0adc0ad0": "theMamaMelon",
        "1c4126846d3e95eb1cadcdd5ec73d071": "noice.com/Deyna",
        "7def921be1436429b5a55883063c8abc": "Mounts Underrrated",
        "845ec72497144b4cd860bec45133baf5": "James I 20 I",
        "bf21cfaacac0c6d01b0fe323ebed9147": "Peter",
        "c1ac0b8ea9d0f5912a5a647c12e7786a": "Mr Testicle Inspecticle",
        "c8e9c90b89c6b8e79dc5f4d8f725cc0c": "ChefHappyTime",
        "d6512957d2d5fa60071fa4d8273e2fde": "Blackhawkftw",
        "e10d42ff26f9000a2ffadcdb04513db7": "edit poly",
        "e4defc4f445a45dea2b6e1627d397eac": "Sefraca",
        "a4c46eb808e2f6dee7f406588a8418f5": "Alex Y",
        "b2075f87717bfbca1e922f081b9e3557": "Jack Bulson"
    }

    # Replace IDs with names where available
    df_interaction["distinct_id"] = df_interaction["distinct_id"].map(mixpanel_lookup).fillna(df_interaction["distinct_id"])
    df_interaction["target_player_id"] = df_interaction["target_player_id"].map(mixpanel_lookup).fillna(df_interaction["target_player_id"])

    # Server filter
    server_options = ['All'] + sorted(df_interaction['server_id'].dropna().unique().tolist())
    selected_server = st.selectbox("Filter by Server (Player Interaction)", server_options)

    filtered_interaction = df_interaction.copy()
    if selected_server != 'All':
        filtered_interaction = filtered_interaction[filtered_interaction['server_id'] == selected_server]

    # 📊 Summary Stats
    unique_attackers = filtered_interaction['distinct_id'].nunique()
    unique_targets = filtered_interaction['target_player_id'].nunique()
    total_kills = len(filtered_interaction)

    st.markdown(f"**🔢 Unique Attackers:** `{unique_attackers}`")
    st.markdown(f"**🎯 Unique Targets:** `{unique_targets}`")
    st.markdown(f"**⚔️ Total Kills Logged:** `{total_kills}`")

    top_killers = (
        filtered_interaction['distinct_id']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Player', 'distinct_id': 'Kills'})
    )

    st.markdown("### 🏆 Top  Killers")
    st.dataframe(top_killers.head(100), use_container_width=True)

    top_weapons = (
        filtered_interaction['item_id']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Weapon', 'item_id': 'Uses'})
    )

    st.markdown("### 🔫 Top Weapons Used")
    st.dataframe(top_weapons.head(30), use_container_width=True)

    # Build graph
    G = nx.DiGraph()
    for _, row in filtered_interaction.iterrows():
        src = row['distinct_id']
        tgt = row['target_player_id']
        if pd.notna(src) and pd.notna(tgt):
            G.add_edge(src, tgt)

    pos = nx.spring_layout(G, seed=42)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#888'), mode='lines')

    node_x, node_y, node_text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition='top center',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[len(list(G.neighbors(n))) for n in G.nodes()],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Outbound Connections',
                xanchor='left'
            ),
            line_width=1
        )
    )

    fig_network = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
        title=dict(text='Player Kills Network Graph'),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    ))

    st.plotly_chart(fig_network, use_container_width=True)

else:
    st.warning("Interaction data must include: 'distinct_id', 'target_player_id', 'server_id', and 'item_id'.")

# ============================
# 🔥 Global Top Player Rivalries
# ============================
st.markdown("---")
st.header("🔥 Top Global Player Rivalries")

# Group kills and deaths
duels = filtered_interaction.groupby(['distinct_id', 'target_player_id']).size().reset_index(name='kills')

# Merge with reversed direction to find mutual kills
rival_duels = pd.merge(
    duels,
    duels,
    left_on=['distinct_id', 'target_player_id'],
    right_on=['target_player_id', 'distinct_id'],
    suffixes=('_from', '_to')
)

# Avoid duplicates (A vs B and B vs A)
rival_duels['sorted_pair'] = rival_duels.apply(lambda row: tuple(sorted([row['distinct_id_from'], row['target_player_id_from']])), axis=1)
rival_duels = rival_duels.drop_duplicates('sorted_pair')

# Rename and organize columns
rivalries_df = rival_duels.rename(columns={
    'distinct_id_from': 'Player A',
    'target_player_id_from': 'Player B',
    'kills_from': 'A → B Kills',
    'kills_to': 'B → A Kills'
})

rivalries_df['Total Kills'] = rivalries_df['A → B Kills'] + rivalries_df['B → A Kills']
rivalries_df['Net Score'] = rivalries_df['A → B Kills'] - rivalries_df['B → A Kills']

# Sort by total interactions
top_rivalries = rivalries_df.sort_values(by='Total Kills', ascending=False).head(20)

st.dataframe(top_rivalries[['Player A', 'Player B', 'A → B Kills', 'B → A Kills', 'Total Kills', 'Net Score']], use_container_width=True)


# ================================
# 🔍 Player Breakdown & Rivalries
# ================================
st.markdown("---")
st.header("🔍 Player Combat Breakdown")

# Collect all unique player names from both attacker and target columns
all_players = sorted(set(df_interaction['distinct_id']).union(df_interaction['target_player_id']))
selected_player = st.selectbox("Select a Player to View Detailed Stats", all_players)

if selected_player:
    # Filter for kills made by the player
    kills = filtered_interaction[filtered_interaction['distinct_id'] == selected_player]
    kills_summary = kills['target_player_id'].value_counts().reset_index()
    kills_summary.columns = ['Target', 'Times Killed']

    # Filter for deaths suffered by the player
    deaths = filtered_interaction[filtered_interaction['target_player_id'] == selected_player]
    deaths_summary = deaths['distinct_id'].value_counts().reset_index()
    deaths_summary.columns = ['Attacker', 'Times Killed By']

    # Summary stats
    total_kills = len(kills)
    total_deaths = len(deaths)

    st.markdown(f"### 📊 Stats for `{selected_player}`")
    st.markdown(f"- **☠️ Kills Made:** `{total_kills}`")
    st.markdown(f"- **💀 Times Killed:** `{total_deaths}`")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ☠️ Players They Killed")
        st.dataframe(kills_summary, use_container_width=True)

    with col2:
        st.markdown("#### 💀 Players Who Killed Them")
        st.dataframe(deaths_summary, use_container_width=True)

    # Bonus: Rivalries
    rivalries = pd.merge(kills_summary, deaths_summary, left_on='Target', right_on='Attacker')
    if not rivalries.empty:
        rivalries['Net Kills'] = rivalries['Times Killed'] - rivalries['Times Killed By']
        rivalries = rivalries.sort_values(by='Net Kills', ascending=False)

        st.markdown("### 🔄 Top Rivalries (Mutual Kill Exchanges)")
        st.dataframe(rivalries[['Target', 'Times Killed', 'Times Killed By', 'Net Kills']], use_container_width=True)
    else:
        st.info("No rivalries found for this player (no mutual kills).")