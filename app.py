import streamlit as st
import utils
import datetime, pytz

st.set_page_config(
    page_title='FPL Analyzer',
    layout='wide',
    initial_sidebar_state='auto'
)

st.title('FPL Analyzer - Home Page')

@st.cache_data(ttl=900, show_spinner=False)
def load_all_data():
    fetched_at = datetime.datetime.now(tz=pytz.timezone("Asia/Kolkata"))
    manager_league_df, manager_details_dict = utils.load_manager_details()
    manager_gw_history = utils.load_manager_gw_history()
    player_json = utils.load_player_data()
    fixtures_json = utils.load_fixtures_data()
    current_gw = utils.get_current_gameweek(player_json)
    pl_teams_dict, pl_teams_list = utils.get_pl_teams_dict_and_list(player_json)
    position_dict = utils.get_position_dict()
    status_dict = utils.get_status_dict()
    player_df = utils.return_player_df(player_json, pl_teams_dict, status_dict, position_dict)
    dreamteam_df, dt_col_defs = utils.get_dream_team(player_df)
    top_price_risers_df, pi_col_defs = utils.return_top_price_risers(player_df)
    top_price_fallers_df, pd_col_defs = utils.return_top_price_fallers(player_df)
    fixtures_df, fixture_col_defs = utils.return_fixtures_df(fixtures_json, pl_teams_dict, player_df)
    fixtures_database = utils.create_team_fixtures_database(fixtures_df, pl_teams_list)
    fdr_database, fdr_avg_coldefs = utils.create_team_fdr_database(fixtures_database)
    team_fdr_rating_df = utils.get_team_FDR_rating(fixtures_df, pl_teams_list)
    pl_table_df, pl_table_col_defs = utils.build_pl_table(pl_teams_list,fixtures_database,utils.get_team_fixtures)

    return {
        "fetched_at": fetched_at,
        "manager_league_df": manager_league_df,
        "manager_details_dict": manager_details_dict,
        "manager_gw_history": manager_gw_history,
        "player_json": player_json,
        "current_gw": current_gw,
        "pl_teams_dict": pl_teams_dict,
        "pl_teams_list": pl_teams_list,
        "position_dict": position_dict,
        "status_dict": status_dict,
        "player_df": player_df,
        "fixtures_df": fixtures_df,
        "dreamteam_df": dreamteam_df,
        "top_price_risers_df": top_price_risers_df,
        "top_price_fallers_df": top_price_fallers_df,
        "fixture_col_defs": fixture_col_defs,
        "fixtures_database": fixtures_database,
        "fdr_database": fdr_database,
        "fdr_avg_coldefs": fdr_avg_coldefs,
        "team_fdr_rating_df": team_fdr_rating_df,
        "pl_table_df" : pl_table_df,
        "pl_table_col_defs" : pl_table_col_defs,
        "dt_col_defs": dt_col_defs,
        "pi_col_defs": pi_col_defs,
        "pd_col_defs": pd_col_defs
    }

with st.sidebar:
    if st.button("Refresh Data"):
        load_all_data.clear()
        st.rerun()

data = load_all_data()

fresh = data["fetched_at"]
manager_league_df = data["manager_league_df"]
manager_details_dict = data["manager_details_dict"]
manager_gw_history = data["manager_gw_history"]
player_json = data["player_json"]
current_gw = data["current_gw"]
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
pl_table_col_defs = data["pl_table_col_defs"]
dreamteam_df = data["dreamteam_df"]
dt_col_defs = data["dt_col_defs"]
top_price_risers_df = data["top_price_risers_df"]
pi_col_defs = data["pi_col_defs"]
top_price_fallers_df = data["top_price_fallers_df"]
pd_col_defs = data["pd_col_defs"]

with st.sidebar:
    st.caption(f"Data last updated: {fresh.strftime('%b %d, %Y %I:%M %p %Z')}")


for key, value in data.items():
    st.session_state[key] = value

st.subheader(f"Welcome, {manager_details_dict['First Name']} {manager_details_dict['Last Name']}!")

utils.render_title_with_bg(f"{manager_details_dict['Team Name']} Summary")

managersum1, managersum2 = st.columns(2)
with managersum1:
    st.metric("Total Points", manager_details_dict['Total Points'], border=True)
with managersum2:
    st.metric("Overall Rank", manager_details_dict['Global Rank'], border=True)