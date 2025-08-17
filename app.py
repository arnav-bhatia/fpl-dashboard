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
    fixtures_json = utils.load_fixtures_data()
    pl_teams_dict, pl_teams_list = utils.get_pl_teams_dict_and_list(player_json)
    position_dict = utils.get_position_dict()
    status_dict = utils.get_status_dict()
    player_df = utils.return_player_df(player_json, pl_teams_dict, status_dict, position_dict)
    fixtures_df, fixture_col_defs = utils.return_fixtures_df(fixtures_json, pl_teams_dict)
    fixtures_database = utils.create_team_fixtures_database(fixtures_df, pl_teams_list)
    
    return {
        "player_json": player_json,
        "pl_teams_dict": pl_teams_dict,
        "pl_teams_list": pl_teams_list,
        "position_dict": position_dict,
        "status_dict": status_dict,
        "player_df": player_df,
        "fixtures_df": fixtures_df,
        "fixture_col_defs": fixture_col_defs,
        "fixtures_database": fixtures_database
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
fixtures_df = data["fixtures_df"]
fixtures_database = data["fixtures_database"]
fixture_col_defs = data["fixture_col_defs"]

# Segment 1
# st.subheader('Top Performers')
utils.render_title_with_bg('Top Performers')

topperformers1, topperformers2 = st.columns(2)

with topperformers1:
    top_performers_options = ['Most Points', 'Best Form', 'Best Value', 'Best Goalkeepers', 'Best Defenders', 'Best Midfielders', 'Best Forwards']
    choose_performer = st.selectbox('Select a category', top_performers_options)
    
    if choose_performer == 'Most Points':
        display_df, coldefs = utils.return_top_players_points(player_df)
    elif choose_performer == 'Best Form':
        display_df, coldefs = utils.return_top_players_form(player_df)
    elif choose_performer == 'Best Value':
        display_df, coldefs = utils.return_top_players_value(player_df)
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

utils.render_title_with_bg('Fixtures')

utils.build_aggrid_table(fixtures_df, pagination=True, max_height=361, col_defs=fixture_col_defs)

fixtures1, fixtures2 = st.columns(2)

with fixtures1:
    team_FDR = st.selectbox('Pick a team', options=pl_teams_list)
    team_FDR_df = utils.get_team_fixtures(team_FDR, fixtures_database)
    utils.build_aggrid_table(team_FDR_df, pagination=True, max_height=361)