from typing import Tuple, Dict, List, Any
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import pandas as pd
from datetime import datetime
import requests
import pytz

# Loading data from FPL API

def load_player_data(PLAYER_URL: str = "https://fantasy.premierleague.com/api/bootstrap-static/") -> Dict[str, Any]:
    """
    Loads player data from the FPL API and returns it in JSON format.

    Args:
        PLAYER_URL (str): URL of the API. Default is the official FPL bootstrap-static endpoint.

    Returns:
        Dict[str, Any]: JSON object containing player data.

    Raises:
        RuntimeError: If there is an HTTP error, timeout, or any other error during the API call.
    """
    try:
        response = requests.get(PLAYER_URL, timeout=10)
        response.raise_for_status()
        player_json = response.json()
        return player_json
    except requests.exceptions.HTTPError as http_err:
        raise RuntimeError(f"HTTP error occurred while fetching player data: {http_err}")
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out while fetching player data.")
    except Exception as err:
        raise RuntimeError(f"An error occurred while fetching player data: {err}")


def load_fixtures_data(FIXTURES_URL: str = "https://fantasy.premierleague.com/api/fixtures/") -> Dict[str, Any]:
    """
    Loads fixture data from the FPL API and returns it in JSON format.

    Args:
        FIXTURES_URL (str): URL of the API. Default is the official FPL fixtures endpoint.

    Returns:
        Dict[str, Any]: JSON object containing fixture data.

    Raises:
        RuntimeError: If there is an HTTP error, timeout, or any other error during the API call.
    """
    try:
        response = requests.get(FIXTURES_URL, timeout=10)
        response.raise_for_status()
        fixtures_json = response.json()
        return fixtures_json
    except requests.exceptions.HTTPError as http_err:
        raise RuntimeError(f"HTTP error occurred while fetching fixture data: {http_err}")
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out while fetching fixture data.")
    except Exception as err:
        raise RuntimeError(f"An error occurred while fetching fixture data: {err}")


# Mapping dictionaries and lists

def get_pl_teams_dict_and_list(player_json: Dict[str, Any]) -> Tuple[Dict[int, str], List[str]]:
    """
    Returns all Premier League teams and their FPL IDs.

    Args:
        player_json (Dict[str, Any]): JSON object containing data from the FPL API.

    Returns:
        Tuple[Dict[int, str], List[str]]: 
            - Dictionary mapping team IDs to team names.
            - List of all team names.
    """
    pl_teams_dict: Dict[int, str] = {}
    pl_teams_list: List[str] = []
    for team in player_json["teams"]:
        pl_teams_dict[team["id"]] = team["name"]
        pl_teams_list.append(team["name"])
    return pl_teams_dict, pl_teams_list


def get_position_dict() -> Dict[int, str]:
    """
    Returns a dictionary mapping FPL position IDs to position names.

    Returns:
        Dict[int, str]: Mapping of FPL position IDs to position names.
    """
    position_dict = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }
    return position_dict


def get_status_dict() -> Dict[str, str]:
    """
    Returns a dictionary mapping FPL status codes to status descriptions.

    Returns:
        Dict[str, str]: Mapping of FPL status codes to descriptions.
    """
    status_dict = {
        'u': 'unavailable',
        'a': 'available',
        'd': 'doubtful',
        'i': 'injured',
        'n': 'not available',
        's': 'suspended'
    }
    return status_dict

# Player and Fixture Dataframes

def return_player_df(
    player_json: Dict[str, Any],
    team_dict: Dict[int, str],
    status_dict: Dict[str, str],
    position_dict: Dict[int, str]
) -> pd.DataFrame:
    """
    Extracts player data from the API JSON and returns a DataFrame.

    Args:
        player_json (Dict[str, Any]): JSON data containing player information.
        team_dict (Dict[int, str]): Mapping of team IDs to team names.
        status_dict (Dict[str, str]): Mapping of status codes to status descriptions.
        position_dict (Dict[int, str]): Mapping of position IDs to position names.

    Returns:
        pd.DataFrame: DataFrame containing player statistics.
    """
    player_database = []
    for player in player_json["elements"]:
        player_row = {
            "ID": player.get("id"),
            "Name": player.get("web_name"),
            "Availability": status_dict.get(player.get("status"), "Unknown"),
            "Position": position_dict.get(player.get("element_type"), "Unknown"),
            "Full Name": f"{player.get('first_name', '')} {player.get('second_name', '')}",
            "Club": team_dict.get(player.get("team"), "Unknown"),
            "Price": float(player.get("now_cost", 0) / 10),
            "Minutes Played": player.get('minutes'),
            "Points": player.get("total_points"),
            'Form': player.get('form'),
            'PPG': player.get('points_per_game'),
            'Value': player.get('value_season'),
            'Selected By (%)': player.get('selected_by_percent'),
            'Goals Scored': player.get('goals_scored'),
            'Assists': player.get('assists'),
            'Clean Sheets': player.get('clean_sheets'),
            'Goals Conceded': player.get('goals_conceded'),
            'Own Goals': player.get('own_goals'),
            'Penalties Saved': player.get('penalties_saved'),
            'Penalties Missed': player.get('penalties_missed'),
            'Yellow Cards': player.get('yellow_cards'),
            'Red Cards': player.get('red_cards'),
            'Saves': player.get('saves'),
            'Bonus': player.get('bonus'),
            'BPS': player.get('bps'),
            'Influence': player.get('influence'),
            'Creativity': player.get('creativity'),
            'Threat': player.get('threat'),
            'ICT Index': player.get('ict_index'),
            'Defensive Contribution': player.get('defensive_contribution', 0),
            'Starts': player.get('starts'),
            'Expected Goals': player.get('expected_goals'),
            'Expected Assists': player.get('expected_assists'),
            'Expected Goal Involvements': player.get('expected_goal_involvements'),
            'Expected Goals Conceded': player.get('expected_goals_conceded'),
            'Influence Rank': player.get('influence_rank'),
            'Influence Rank Type': player.get('influence_rank_type'),
            'Creativity Rank': player.get('creativity_rank'),
            'Creativity Rank Type': player.get('creativity_rank_type'),
            'Threat Rank': player.get('threat_rank'),
            'Threat Rank Type': player.get('threat_rank_type'),
            'ICT Index Rank': player.get('ict_index_rank'),
            'ICT Index Rank Type': player.get('ict_index_rank_type'),
            'Expected Goals per 90': player.get('expected_goals_per_90'),
            'Saves per 90': player.get('saves_per_90'),
            'Expected Assists per 90': player.get('expected_assists_per_90'),
            'Expected Goal Involvement per 90': player.get('expected_goal_involvements_per_90'),
            'Expected Goals Conceded per 90': player.get('expected_goals_conceded_per_90'),
            'Goals Conceded per 90': player.get('goals_conceded_per_90'),
            'Form Rank': player.get('form_rank'),
            'Form Rank Type': player.get('form_rank_type'),
            'Points per Game Rank': player.get('points_per_game_rank'),
            'Points per Game Rank Type': player.get('points_per_game_rank_type'),
            'Clean Sheets per 90': player.get('clean_sheets_per_90'),
        }
        player_database.append(player_row)

    return pd.DataFrame(player_database)


# ------------------- Helper functions for fixtures -------------------

def convert_utc_to_ist(datetime_str: str) -> datetime:
    """
    Converts UTC time string to IST datetime.

    Args:
        datetime_str (str): UTC datetime in ISO format.

    Returns:
        datetime: Datetime object converted to IST.
    """
    utc_time = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
    return utc_time.astimezone(pytz.timezone('Asia/Kolkata'))


def get_match_date(datetime_str: str) -> str:
    """
    Converts UTC datetime string to IST date string.

    Args:
        datetime_str (str): UTC datetime in ISO format.

    Returns:
        str: Date in YYYY-MM-DD format.
    """
    return convert_utc_to_ist(datetime_str).strftime('%Y-%m-%d')


def get_match_time(datetime_str: str) -> str:
    """
    Converts UTC datetime string to IST time string.

    Args:
        datetime_str (str): UTC datetime in ISO format.

    Returns:
        str: Time in hh:mm(am/pm) format.
    """
    return convert_utc_to_ist(datetime_str).strftime('%I:%M%p').lstrip('0').lower()


def return_fixtures_df(fixtures_json: List[Dict[str, Any]], team_dict: Dict[int, str]) -> pd.DataFrame:
    """
    Converts fixture JSON into a DataFrame.

    Args:
        fixtures_json (List[Dict[str, Any]]): List of fixture dictionaries.
        team_dict (Dict[int, str]): Mapping of team IDs to team names.

    Returns:
        pd.DataFrame: DataFrame containing fixture details.
    """
    fixtures = []
    for match in fixtures_json:
        home_team = team_dict.get(match.get("team_h"), "Unknown")
        away_team = team_dict.get(match.get("team_a"), "Unknown")

        match_dict = {
            "Gameweek": match.get("event"),
            "Home Team": home_team,
            "Home Team Difficulty": match.get('team_h_difficulty'),
            "Away Team": away_team,
            "Away Team Difficulty": match.get('team_a_difficulty'),
            "Date": match.get('kickoff_time'),
            "Score": f"{match.get('team_h_score', 0)} : {match.get('team_a_score', 0)}"
        }
        fixtures.append(match_dict)

    fixtures_df = pd.DataFrame(fixtures)
    fixtures_df['Match Date'] = fixtures_df['Date'].apply(get_match_date)
    fixtures_df['Match Time (IST)'] = fixtures_df['Date'].apply(get_match_time)
    fixtures_df.drop('Date', axis=1, inplace=True)
    return fixtures_df


def create_team_fixtures_database(fixtures_df: pd.DataFrame, team_list: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Creates a dictionary of DataFrames containing fixtures for each team.

    Args:
        fixtures_df (pd.DataFrame): DataFrame containing all fixtures.
        team_list (List[str]): List of all team names.

    Returns:
        Dict[str, pd.DataFrame]: Mapping of team name to their fixtures DataFrame.
    """
    team_fixtures_database = {}

    for team in team_list:
        team_fixtures = fixtures_df[(fixtures_df['Home Team'] == team) | (fixtures_df['Away Team'] == team)].reset_index(drop=True)
        team_fixture_list = []

        for gw in range(len(team_fixtures)):
            game = team_fixtures.iloc[gw]
            if game['Home Team'] == team:
                venue = 'Home'
                opponent = game['Away Team']
                difficulty = game['Home Team Difficulty']
            else:
                venue = 'Away'
                opponent = game['Home Team']
                difficulty = game['Away Team Difficulty']

            gw_dict = {
                "Game Week": game['Gameweek'],
                "Opponent": opponent,
                "Venue": venue,
                'Fixture Difficulty Rating': int(difficulty) if difficulty is not None else None,
                'Date': game['Match Date'],
                'Time (IST)': game['Match Time (IST)']
            }
            team_fixture_list.append(gw_dict)

        team_fixture_df = pd.DataFrame(team_fixture_list)
        team_fixtures_database[team] = team_fixture_df

    return team_fixtures_database


def get_team_fixtures(team: str, team_fixtures_database: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Retrieves fixtures for a specific team.

    Args:
        team (str): Name of the team.
        team_fixtures_database (Dict[str, pd.DataFrame]): Mapping of team name to their fixtures DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the team's fixtures.
    """
    return team_fixtures_database.get(team, pd.DataFrame())

def return_top_players_points(player_database: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return the top players across all positions based on total points.

    Args:
        player_database (pd.DataFrame): DataFrame containing player data.
        top_n (int, optional): Number of top players to return. Defaults to 10.

    Returns:
        pd.DataFrame: DataFrame of the top players sorted by total points.
    """
    cols = ['Name', 'Club', 'Position', 'Price', 'Minutes Played', 
            'Selected By (%)', 'Form', 'Value', 'PPG', 'Points']
    
    return (
        player_database[cols]
        .sort_values(by='Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def return_top_goalkeepers(player_database: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return the top goalkeepers based on total points.

    Args:
        player_database (pd.DataFrame): DataFrame containing player data.
        top_n (int, optional): Number of top goalkeepers to return. Defaults to 10.

    Returns:
        pd.DataFrame: DataFrame of the top goalkeepers sorted by total points.
    """
    cols = ['Name', 'Club', 'Price', 'Starts', 'Selected By (%)', 
            'Form', 'Value', 'Clean Sheets', 'Goals Conceded', 
            'Saves', 'Saves per 90', 'BPS', 'Points']
    
    return (
        player_database[player_database['Position'] == 'Goalkeeper'][cols]
        .sort_values(by='Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def return_top_defenders(player_database: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return the top defenders based on total points.

    Args:
        player_database (pd.DataFrame): DataFrame containing player data.
        top_n (int, optional): Number of top defenders to return. Defaults to 10.

    Returns:
        pd.DataFrame: DataFrame of the top defenders sorted by total points.
    """
    cols = ['Name', 'Club', 'Price', 'Starts', 'Selected By (%)', 
            'Form', 'Value', 'Clean Sheets', 'Goals Conceded', 
            'Defensive Contribution', 'ICT Index', 'ICT Index Rank Type', 
            'Assists', 'Goals Scored', 'Points']
    
    return (
        player_database[player_database['Position'] == 'Defender'][cols]
        .sort_values(by='Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def return_top_midfielders(player_database: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return the top midfielders based on total points.

    Args:
        player_database (pd.DataFrame): DataFrame containing player data.
        top_n (int, optional): Number of top midfielders to return. Defaults to 10.

    Returns:
        pd.DataFrame: DataFrame of the top midfielders sorted by total points.
    """
    cols = ['Name', 'Club', 'Price', 'Starts', 'Selected By (%)', 
            'Form', 'Value', 'Defensive Contribution', 
            'Expected Goal Involvements', 'ICT Index', 
            'ICT Index Rank Type', 'Assists', 'Goals Scored', 'Points']
    
    return (
        player_database[player_database['Position'] == 'Midfielder'][cols]
        .sort_values(by='Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def return_top_forwards(player_database: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return the top forwards based on total points.

    Args:
        player_database (pd.DataFrame): DataFrame containing player data.
        top_n (int, optional): Number of top forwards to return. Defaults to 10.

    Returns:
        pd.DataFrame: DataFrame of the top forwards sorted by total points.
    """
    cols = ['Name', 'Club', 'Price', 'Starts', 'Selected By (%)', 
            'Form', 'Value', 'Expected Goal Involvements', 
            'ICT Index', 'ICT Index Rank Type', 'Assists', 
            'Expected Goals', 'Goals Scored', 'Points']
    
    return (
        player_database[player_database['Position'] == 'Forward'][cols]
        .sort_values(by='Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

def build_aggrid_table(df):
    """
    Builds and displays an AgGrid table with polished styling:
    - Alternating row colors
    - Colored column headers
    - Auto-sized columns
    - Sortable, filterable, resizable columns

    Args:
        df (pd.DataFrame): DataFrame to display in AgGrid.

    Returns:
        AgGrid: Streamlit AgGrid table component.
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Enable pagination
    gb.configure_pagination(paginationAutoPageSize=True)
    
    # Default column config
    gb.configure_default_column(resizable=True, sortable=True, filter=True, autoSizeColumns=True)
    
    # Alternating row colors using JsCode
    row_style = JsCode("""
        function(params) {
            if (params.node.rowIndex % 2 === 0) {
                return {'background-color': '#f9f9f9'};
            } else {
                return {'background-color': '#ffffff'};
            }
        }
    """)
    gb.configure_grid_options(getRowStyle=row_style)
    
    # Header style using JsCode
    header_style = JsCode("""
        function(params) {
            params.column.getColDef().headerClass = 'header-blue';
        }
    """)

    for col in df.columns:
        gb.configure_column(col, header_class=header_style)

    grid_options = gb.build()

    custom_css = [
        {
            "selector": ".header-blue",
            "rule": "background-color: #1976d2; color: white; font-weight: bold;"
        }
    ]

    return AgGrid(
        df,
        gridOptions=grid_options,
        height=370,
        fit_columns_on_grid_load=True,
        theme='fresh',
        allow_unsafe_jscode=True,
        custom_css=custom_css
    )