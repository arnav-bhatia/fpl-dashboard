import streamlit as st
import utils
import pathlib

st.set_page_config(
    page_title='FPL Analyzer',
    layout='wide',
    initial_sidebar_state='auto'
)

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

st.title('FPL Analyzer')

@st.cache_data
def load_all_data():
    player_json = utils.load_player_data()
    fixtures_json = utils.load_fixtures_data()
    pl_teams_dict, pl_teams_list = utils.get_pl_teams_dict_and_list(player_json)
    position_dict = utils.get_position_dict()
    status_dict = utils.get_status_dict()
    player_df = utils.return_player_df(player_json, pl_teams_dict, status_dict, position_dict)
    fixtures_df, fixture_col_defs = utils.return_fixtures_df(fixtures_json, pl_teams_dict, player_df)
    fixtures_database = utils.create_team_fixtures_database(fixtures_df, pl_teams_list)
    fdr_database, fdr_avg_coldefs = utils.create_team_fdr_database(fixtures_database)
    team_fdr_rating_df = utils.get_team_FDR_rating(fixtures_database, pl_teams_list)
    pl_table_df = utils.build_pl_table(pl_teams_list, fixtures_database, utils.get_team_fixtures)
    
    return {
        "player_json": player_json,
        "pl_teams_dict": pl_teams_dict,
        "pl_teams_list": pl_teams_list,
        "position_dict": position_dict,
        "status_dict": status_dict,
        "player_df": player_df,
        "fixtures_df": fixtures_df,
        "fixture_col_defs": fixture_col_defs,
        "fixtures_database": fixtures_database,
        "fdr_database": fdr_database,
        "fdr_avg_coldefs": fdr_avg_coldefs,
        "team_fdr_rating_df": team_fdr_rating_df,
        "pl_table_df" : pl_table_df
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
fdr_database = data["fdr_database"]
fdr_avg_coldefs = data["fdr_avg_coldefs"]
team_fdr_rating_df = data["team_fdr_rating_df"]
pl_table_df = data["pl_table_df"]

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

utils.render_title_with_bg('Fixtures and Results')

utils.build_aggrid_table(fixtures_df, pagination=True, max_height=370, col_defs=fixture_col_defs)

utils.render_divider()

utils.render_title_with_bg('Fixture Difficulty Rating')

fixtures1, fixtures2, fixtures3 = st.columns([1, 2, 1])

with fixtures1:
    utils.render_subheaders('Teams with lowest FDR', margin_top=5, margin_bottom=17)
    utils.build_aggrid_table(fdr_database, pagination=True, max_height=370, col_defs=fdr_avg_coldefs)
    
with fixtures2:
    team_FDR = st.selectbox(
        '', 
        options=pl_teams_list, 
        placeholder="Choose a team", 
        label_visibility='collapsed',
        key="select-box"
    )
    team_FDR_df, fdr_coldefs = utils.get_team_fixtures(team_FDR, fixtures_database)
    utils.build_aggrid_table(team_FDR_df, pagination=True, max_height=370, col_defs=fdr_coldefs, alt_row_colours=False, FDR=True)
    
with fixtures3:
    utils.render_subheaders(f"{team_FDR}'s FDR Metrics", margin_top=5, margin_bottom=17)
    home_value = team_fdr_rating_df[team_fdr_rating_df['Team'] == team_FDR]['Home FDR'].iloc[0]
    away_value = team_fdr_rating_df[team_fdr_rating_df['Team'] == team_FDR]['Away FDR'].iloc[0]
    
    fdr_home_base_key = utils.map_fdr_colour(home_value)
    fdr_away_base_key = utils.map_fdr_colour(away_value)

    unique_home_key = f"{fdr_home_base_key}_home"
    unique_away_key = f"{fdr_away_base_key}_away"

    col1, col2 = st.columns(2)

    with col1:
        with st.container(key=unique_home_key):
            st.metric(f'{team_FDR} at Home', home_value, border=True)

    with col2:
        with st.container(key=unique_away_key):
            st.metric(f'{team_FDR} Away', away_value, border=True)
    with st.container(key="fdr-metric"):
        team_5gw_avg_fdr = fdr_database[fdr_database['Team']==team_FDR]['5 GW FDR Avg'].iloc[0]
        team_10gw_avg_fdr = fdr_database[fdr_database['Team']==team_FDR]['10 GW FDR Avg'].iloc[0]
        team_5gw_rank = int(fdr_database[fdr_database['Team']==team_FDR]['5 GW FDR Avg'].index[0])
        team_10gw_rank = int(fdr_database[fdr_database['Team']==team_FDR]['10 GW FDR Avg'].index[0])
        delta_colour_5 = utils.calc_fdr_delta_colour(team_5gw_rank)
        delta_colour_10 = utils.calc_fdr_delta_colour(team_10gw_rank)
        st.metric(f"Average FDR for the next 5 GWs", team_5gw_avg_fdr, delta=f"PL Rank: {team_5gw_rank}", delta_color=delta_colour_5, border=True)
        st.metric(f"Average FDR for the next 10 GWs", team_10gw_avg_fdr, delta=f"PL Rank: {team_10gw_rank}", delta_color=delta_colour_5, border=True)

utils.render_divider()

utils.render_title_with_bg('Premier League Table')

utils.build_aggrid_table(pl_table_df)
