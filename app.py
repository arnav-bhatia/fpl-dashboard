import streamlit as st
import utils

st.set_page_config(
    page_title='FPL Analyzer',
    layout='wide',
    initial_sidebar_state='auto'
)

st.title('FPL Analyzer')

# Setup
@st.cache_data
def load_all_data():
    player_json = utils.load_player_data()
    pl_teams_dict, pl_teams_list = utils.get_pl_teams_dict_and_list(player_json)
    position_dict = utils.get_position_dict()
    status_dict = utils.get_status_dict()
    player_df = utils.return_player_df(player_json, pl_teams_dict, status_dict, position_dict)
    
    return {
        "player_json": player_json,
        "pl_teams_dict": pl_teams_dict,
        "pl_teams_list": pl_teams_list,
        "position_dict": position_dict,
        "status_dict": status_dict,
        "player_df": player_df
    }

if st.button("Refresh Data"):
    load_all_data.clear()
    st.rerun()

data = load_all_data()

player_json = data["player_json"]
pl_teams_dict = data["pl_teams_dict"]
pl_teams_list = data["pl_teams_list"]
position_dict = data["position_dict"]
status_dict = data["status_dict"]
player_df = data["player_df"]

# Segment 1
# st.subheader('Top Performers')
utils.render_title_with_bg('Top Performers')

topperformers1, topperformers2 = st.columns(2)

with topperformers1:
    top_performers_options = ['Most Points', 'Best Goalkeepers', 'Best Defenders', 'Best Midfielders', 'Best Forwards']
    choose_performer = st.selectbox('Select a category', top_performers_options)

    if choose_performer == 'Most Points':
        display_df, coldefs = utils.return_top_players_points(player_df)
    elif choose_performer == 'Best Goalkeepers':
        display_df, coldefs = utils.return_top_goalkeepers(player_df)
    elif choose_performer == 'Best Defenders':
        display_df, coldefs = utils.return_top_defenders(player_df)
    elif choose_performer == 'Best Midfielders':
        display_df, coldefs = utils.return_top_midfielders(player_df)
    else:
        display_df, coldefs = utils.return_top_forwards(player_df)
        
    utils.build_aggrid_table(display_df, col_defs=coldefs)
with topperformers2:
    player_cards_dict = utils.get_top_stats_for_player_cards(player_df)
    row1 = st.columns(3)
    row2 = st.columns(3)

    for i, (label, df_row) in enumerate(player_cards_dict.items()):
        player_row = df_row.iloc[0]
        stat_value = player_row[label]

        col = row1[i] if i < 3 else row2[i-3]
        with col:
            utils.render_player_card(player_row, label, stat_value)

utils.render_divider()