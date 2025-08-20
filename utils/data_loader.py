from typing import Tuple, Dict, List, Any
from st_aggrid import JsCode
import streamlit as st
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
            "Total Points": player.get("total_points"),
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
            'photo_code': player.get('code'),
            'Defensive Contributions': player.get('defensive_contribution', 0),
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


def return_fixtures_df(fixtures_json: List[Dict[str, Any]], team_dict: Dict[int, str], player_df) -> pd.DataFrame:
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
        h_a = ['h', 'a']
        home_goals = []
        away_goals = []
        home_assists = []
        away_assists = []
        bonus_getters = []
        home_team = team_dict.get(match.get("team_h"), "Unknown")
        away_team = team_dict.get(match.get("team_a"), "Unknown")

        try:
            goals_scored = match['stats'][0]
            assists = match['stats'][1]

            for team in h_a:
                # Goals
                if goals_scored[team]:
                    for goal in goals_scored[team]:
                        player_id = goal['element']
                        player = player_df.loc[player_df['ID'] == player_id, 'Name'].iloc[0]
                        goals = goal['value']
                        if team == 'h':
                            home_goals.append(f"{player}({goals})")
                        else:
                            away_goals.append(f"{player}({goals})")

                # Assists
                if assists[team]:
                    for assist in assists[team]:
                        player_id = assist['element']
                        player = player_df.loc[player_df['ID'] == player_id, 'Name'].iloc[0]
                        assisted = assist['value']
                        if team == 'h':
                            home_assists.append(f"{player}({assisted})")
                        else:
                            away_assists.append(f"{player}({assisted})")
        except:
            pass

        
        try:
            bonus = match['stats'][8]
            temp_bonus = []
            for team in h_a:
                if bonus[team]:
                    for bp in bonus[team]:
                        player_id = bp['element']
                        player = player_df.loc[player_df['ID'] == player_id, 'Name'].iloc[0]
                        bp_received = int(bp['value'])
                        temp_bonus.append((player, bp_received))

            temp_bonus.sort(key=lambda x: x[1], reverse=True)
            bonus_getters = [f"{player}({bp})" for player, bp in temp_bonus]

        except:
            pass

        match_dict = {
            "Gameweek": match.get("event"),
            "Home Team": home_team,
            "Home Team Difficulty": match.get('team_h_difficulty'),
            "Away Team": away_team,
            "Away Team Difficulty": match.get('team_a_difficulty'),
            "Date": match.get('kickoff_time'),
            "Score": f"{match.get('team_h_score')} : {match.get('team_a_score')}",
            "Home Team Scorers": ", ".join(home_goals) if home_goals else "",
            "Away Team Scorers": ", ".join(away_goals) if away_goals else "",
            "Home Team Assisters": ", ".join(home_assists) if home_assists else "",
            "Away Team Assisters": ", ".join(away_assists) if away_assists else "",
            "Bonus Points": ", ".join(bonus_getters) if bonus_getters else "",
        }

        fixtures.append(match_dict)

    fixtures_df = pd.DataFrame(fixtures)
    fixtures_df.loc[fixtures_df['Score'] == 'None : None', 'Score'] = 'Yet to Happen'
    fixtures_df['Match Date'] = fixtures_df['Date'].apply(get_match_date)
    fixtures_df['Match Time (IST)'] = fixtures_df['Date'].apply(get_match_time)
    fixtures_df.drop('Date', axis=1, inplace=True)
    
    fixtures_col_defs = [
        {"headerName": "GW", "field": "Gameweek", "flex": 1, "minWidth": 70},
        {"headerName": "Home Team", "field": "Home Team", "flex": 1.5, "minWidth": 100},
        {"headerName": "Away Team", "field": "Away Team", "flex": 1.5, "minWidth": 100},
        {"headerName": "Score", "field": "Score", "flex": 2, "minWidth": 70, "cellStyle": {"font-weight": "bold"}},
        {"headerName": "Date", "field": "Match Date", "flex": 1, "minWidth": 70},
        {"headerName": "Time (IST)", "field": "Match Time (IST)", "flex": 1, "minWidth": 70},        {"headerName": "Home Scorers", "field": "Home Team Scorers", "flex": 2, "minWidth": 100},
        {"headerName": "Away Scorers", "field": "Away Team Scorers", "flex": 2, "minWidth": 100},
        {"headerName": "Home Assisters", "field": "Home Team Assisters", "flex": 2, "minWidth": 100},
        {"headerName": "Away Assisters", "field": "Away Team Assisters", "flex": 2, "minWidth": 100},
        {"headerName": "Bonus Points", "field": "Bonus Points", "flex": 2, "minWidth": 140},
    ]

    return fixtures_df, fixtures_col_defs


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
                'Time (IST)': game['Match Time (IST)'],
                "Score": game['Score'],

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
    team_df = team_fixtures_database.get(team, pd.DataFrame())
    cols_to_str = ['Game Week', 'Fixture Difficulty Rating']
    team_df[cols_to_str] = team_df[cols_to_str].astype(str)

    col_defs = [
        {"headerName": "GW", "field": "Game Week", "flex": 1, "minWidth": 70},
        {"headerName": "Opponent", "field": "Opponent", "flex": 2, "minWidth": 160, "cellStyle": {"font-weight": "bold"}},
        {"headerName": "Venue", "field": "Venue", "flex": 1, "minWidth": 100},
        {"headerName": "FDR", "field": "Fixture Difficulty Rating", "flex": 1, "minWidth": 70, "cellStyle": {"font-weight": "bold"}},
        {"headerName": "Date", "field": "Date", "flex": 1, "minWidth": 100},
        {"headerName": "Time (IST)", "field": "Time (IST)", "flex": 1, "minWidth": 100},
        {"headerName": "Score", "field": "Score", "flex": 2, "minWidth": 120},
    ]

    return team_df, col_defs

def get_team_FDR_rating(team_fixtures_database, team_list):
    arsenal_fixtures = team_fixtures_database['Arsenal']
    aston_villa_fixtures = team_fixtures_database['Aston Villa']
    team_fdr_rating_list = []
    for team in team_list:
        if team != 'Arsenal':
            match_away = arsenal_fixtures[(arsenal_fixtures['Opponent']==team) & (arsenal_fixtures['Venue']=='Away')]
            match_home = arsenal_fixtures[(arsenal_fixtures['Opponent']==team) & (arsenal_fixtures['Venue']=='Home')]
            team_fdr_rating = {
                'Team': match_home['Opponent'].iloc[0],
                'Home FDR': match_home['Fixture Difficulty Rating'].iloc[0],
                'Away FDR': match_away['Fixture Difficulty Rating'].iloc[0]
            }
            team_fdr_rating_list.append(team_fdr_rating)
        else:
            match_away = aston_villa_fixtures[(aston_villa_fixtures['Opponent']=='Arsenal') & (aston_villa_fixtures['Venue']=='Away')]
            match_home = aston_villa_fixtures[(aston_villa_fixtures['Opponent']=='Arsenal') & (aston_villa_fixtures['Venue']=='Home')]
            team_fdr_rating = {
                'Team': match_home['Opponent'].iloc[0],
                'Home FDR': match_home['Fixture Difficulty Rating'].iloc[0],
                'Away FDR': match_away['Fixture Difficulty Rating'].iloc[0]
            }
            team_fdr_rating_list.append(team_fdr_rating)
    team_fdr_rating_df = pd.DataFrame(team_fdr_rating_list)
    return team_fdr_rating_df
            
def create_team_fdr_database(team_fixtures_database):
    fdr_list = []
    for team in team_fixtures_database:
        df = team_fixtures_database[team]
        df = df[df['Score'] == 'Yet to Happen']
        df['Fixture Difficulty Rating'] = df['Fixture Difficulty Rating'].apply(pd.to_numeric)
        avg_5 = round(df.head(5)['Fixture Difficulty Rating'].mean(), 2)
        avg_10 = round(df.head(10)['Fixture Difficulty Rating'].mean(), 2)
        team_fdr_avg = {
            'Team' : team,
            '5 GW FDR Avg' : avg_5,
            '10 GW FDR Avg' : avg_10
        }
        fdr_list.append(team_fdr_avg)
    
    fdr_avg_df = pd.DataFrame(fdr_list)
    fdr_avg_df = fdr_avg_df.sort_values(by='5 GW FDR Avg')
    fdr_avg_df = fdr_avg_df.reset_index(drop=True)
    fdr_avg_df.index = range(1, 21)
    
    col_defs = [
        {"headerName": "Club", "field": "Team", "flex": 2, "minWidth": 140, "cellStyle": {"font-weight": "bold"}},
        {"headerName": "5 Gameweek Avg", "field": "5 GW FDR Avg", "flex": 1, "minWidth": 100},
        {"headerName": "10 Gameweek Avg", "field": "10 GW FDR Avg", "flex": 1, "minWidth": 100},
    ]
    
    return fdr_avg_df, col_defs

def return_top_players_points(player_database: pd.DataFrame, top_n: int = 10) -> tuple:
    cols = ['Name', 'Club', 'Position', 'Price', 'Minutes Played', 'BPS', 
            'Selected By (%)', 'Form', 'Value', 'PPG', 'Total Points']
    
    df = (
        player_database[cols]
        .sort_values(by='Total Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # Define col_defs for AgGrid
    col_defs = [
        {"headerName": "Name", "field": "Name", "flex": 2, "minWidth": 100, "pinned": "left", "cellStyle": {"font-weight": "bold", "text-transform": "uppercase"}},
        {"headerName": "Club", "field": "Club", "flex": 1, "minWidth": 100},
        {"headerName": "Position", "field": "Position", "flex": 1, "minWidth": 90},
        {"headerName": "Price", "field": "Price", "flex": 1, "minWidth": 70},
        {"headerName": "Points", "field": "Total Points", "flex": 1, "minWidth": 70, "cellStyle": {"font-weight": "bold"}},
        {"headerName": "SBP", "field": "Selected By (%)", "flex": 1, "minWidth": 70},
        {"headerName": "MP", "field": "Minutes Played", "flex": 1, "minWidth": 70},    
        {"headerName": "Form", "field": "Form", "flex": 1, "minWidth": 70},
        {"headerName": "PPG", "field": "PPG", "flex": 1, "minWidth": 70},
        {"headerName": "Value", "field": "Value", "flex": 1, "minWidth": 70},
        {"headerName": "BPS", "field": "BPS", "flex": 1, "minWidth": 70},
    ]
    
    return df, col_defs

def return_top_players_form(player_database: pd.DataFrame, top_n: int = 10) -> tuple:
    player_database = player_database.copy()
    player_database['Form'] = pd.to_numeric(player_database['Form'], errors='coerce')
    
    cols = ['Name', 'Club', 'Position', 'Price', 'Minutes Played', 'BPS', 
            'Selected By (%)', 'Form', 'Value', 'PPG', 'Total Points']
    df = (
        player_database[cols]
        .sort_values(by='Form', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # Define col_defs for AgGrid
    col_defs = [
        {"headerName": "Name", "field": "Name", "flex": 2, "minWidth": 100, "pinned": "left", "cellStyle": {"font-weight": "bold", "text-transform": "uppercase"}},
        {"headerName": "Club", "field": "Club", "flex": 1, "minWidth": 100},
        {"headerName": "Position", "field": "Position", "flex": 1, "minWidth": 90},
        {"headerName": "Form", "field": "Form", "flex": 1, "minWidth": 70, "cellStyle": { "font-weight": "bold"}},
        {"headerName": "Price", "field": "Price", "flex": 1, "minWidth": 70},
        {"headerName": "Points", "field": "Total Points", "flex": 1, "minWidth": 70},
        {"headerName": "SBP", "field": "Selected By (%)", "flex": 1, "minWidth": 70},
        {"headerName": "MP", "field": "Minutes Played", "flex": 1, "minWidth": 70},    
        {"headerName": "PPG", "field": "PPG", "flex": 1, "minWidth": 70},
        {"headerName": "Value", "field": "Value", "flex": 1, "minWidth": 70},
        {"headerName": "BPS", "field": "BPS", "flex": 1, "minWidth": 70},
    ]
    
    return df, col_defs

def return_top_players_value(player_database: pd.DataFrame, top_n: int = 10) -> tuple:
    cols = ['Name', 'Club', 'Position', 'Price', 'Minutes Played', 'BPS', 
            'Selected By (%)', 'Form', 'Value', 'PPG', 'Total Points']
    
    df = (
        player_database[cols]
        .sort_values(by='Value', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # Define col_defs for AgGrid
    col_defs = [
        {"headerName": "Name", "field": "Name", "flex": 2, "minWidth": 100, "pinned": "left", "cellStyle": {"font-weight": "bold", "text-transform": "uppercase"}},
        {"headerName": "Club", "field": "Club", "flex": 1, "minWidth": 100},
        {"headerName": "Position", "field": "Position", "flex": 1, "minWidth": 90},
        {"headerName": "Value", "field": "Value", "flex": 1, "minWidth": 70, "cellStyle": { "font-weight": "bold"}},
        {"headerName": "Price", "field": "Price", "flex": 1, "minWidth": 70},
        {"headerName": "Points", "field": "Total Points", "flex": 1, "minWidth": 70},
        {"headerName": "Form", "field": "Form", "flex": 1, "minWidth": 70},
        {"headerName": "SBP", "field": "Selected By (%)", "flex": 1, "minWidth": 70},
        {"headerName": "MP", "field": "Minutes Played", "flex": 1, "minWidth": 70},    
        {"headerName": "PPG", "field": "PPG", "flex": 1, "minWidth": 70},
        {"headerName": "BPS", "field": "BPS", "flex": 1, "minWidth": 70},
    ]
    
    return df, col_defs

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
            'Saves', 'BPS', 'Total Points']
    
    df = (
        player_database[player_database['Position'] == 'Goalkeeper'][cols]
        .sort_values(by='Total Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    col_defs = [
        {"headerName": "Name", "field": "Name", "flex": 2, "minWidth": 100, "pinned": "left", "cellStyle": {"font-weight": "bold", "text-transform": "uppercase"}},
        {"headerName": "Club", "field": "Club", "flex": 1, "minWidth": 100},
        {"headerName": "Price", "field": "Price", "flex": 1, "minWidth": 70},
        {"headerName": "Points", "field": "Total Points", "flex": 1, "minWidth": 70, "cellStyle": { "font-weight": "bold"}},
        {"headerName": "CS", "field": "Clean Sheets", "flex": 1, "minWidth": 50, "maxWidth": 90},
        {"headerName": "Saves", "field": "Saves", "flex": 1, "minWidth": 70},
        {"headerName": "GC", "field": "Goals Conceded", "flex": 1, "minWidth": 70},
        {"headerName": "SBP", "field": "Selected By (%)", "flex": 1, "minWidth": 70},
        {"headerName": "Starts", "field": "Starts", "flex": 1, "minWidth": 70},    
        {"headerName": "Form", "field": "Form", "flex": 1, "minWidth": 70},
        {"headerName": "Value", "field": "Value", "flex": 1, "minWidth": 70},
        {"headerName": "BPS", "field": "BPS", "flex": 1, "minWidth": 70},
    ]
    
    return df, col_defs

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
            'Defensive Contributions', 'ICT Index', 'ICT Index Rank Type', 
            'Assists', 'Goals Scored', 'Total Points', 'BPS']
    
    df =  (
        player_database[player_database['Position'] == 'Defender'][cols]
        .sort_values(by='Total Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    col_defs = [
        {"headerName": "Name", "field": "Name", "flex": 2, "minWidth": 100, "pinned": "left", "cellStyle": {"font-weight": "bold", "text-transform": "uppercase"}},
        {"headerName": "Club", "field": "Club", "flex": 1, "minWidth": 100},
        {"headerName": "Price", "field": "Price", "flex": 1, "minWidth": 70},
        {"headerName": "Points", "field": "Total Points", "flex": 1, "minWidth": 70, "cellStyle": { "font-weight": "bold"}},
        {"headerName": "Starts", "field": "Starts", "flex": 1, "minWidth": 70},
        {"headerName": "CS", "field": "Clean Sheets", "flex": 1, "minWidth": 50, "maxWidth": 90},
        {"headerName": "GC", "field": "Goals Conceded", "flex": 1, "minWidth": 70},
        {"headerName": "DC", "field": "Defensive Contribution", "flex": 1, "minWidth": 70},
        {"headerName": "SBP", "field": "Selected By (%)", "flex": 1, "minWidth": 70},
        {"headerName": "ICT", "field": "ICT Index", "flex": 1, "minWidth": 70},
        {"headerName": "ICT Rank", "field": "ICT Index Rank Type", "flex": 1, "minWidth": 70},
        {"headerName": "Assists", "field": "Assists", "flex": 1, "minWidth": 70},
        {"headerName": "Goals", "field": "Goals Scored", "flex": 1, "minWidth": 70},
        {"headerName": "Form", "field": "Form", "flex": 1, "minWidth": 70},
        {"headerName": "Value", "field": "Value", "flex": 1, "minWidth": 70},
        {"headerName": "BPS", "field": "BPS", "flex": 1, "minWidth": 70},    
    ]
    
    return df, col_defs


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
            'Form', 'Value', 'Defensive Contributions', 
            'Expected Goal Involvements', 'ICT Index', 'BPS',
            'ICT Index Rank Type', 'Assists', 'Goals Scored', 'Total Points']
    
    df =  (
        player_database[player_database['Position'] == 'Midfielder'][cols]
        .sort_values(by='Total Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    col_defs = [
        {"headerName": "Name", "field": "Name", "flex": 2, "minWidth": 100, "pinned": "left", "cellStyle": {"font-weight": "bold", "text-transform": "uppercase"}},
        {"headerName": "Club", "field": "Club", "flex": 1, "minWidth": 100},
        {"headerName": "Price", "field": "Price", "flex": 1, "minWidth": 70},
        {"headerName": "Points", "field": "Total Points", "flex": 1, "minWidth": 70, "cellStyle": { "font-weight": "bold"}},
        {"headerName": "Starts", "field": "Starts", "flex": 1, "minWidth": 70},
        {"headerName": "xGI", "field": "Expected Goal Involvements", "flex": 1, "minWidth": 70},
        {"headerName": "DC", "field": "Defensive Contributions", "flex": 1, "minWidth": 70},
        {"headerName": "SBP", "field": "Selected By (%)", "flex": 1, "minWidth": 70},
        {"headerName": "ICT", "field": "ICT Index", "flex": 1, "minWidth": 70},
        {"headerName": "ICT Rank", "field": "ICT Index Rank Type", "flex": 1, "minWidth": 70},
        {"headerName": "Assists", "field": "Assists", "flex": 1, "minWidth": 70},
        {"headerName": "Goals", "field": "Goals Scored", "flex": 1, "minWidth": 70},
        {"headerName": "Form", "field": "Form", "flex": 1, "minWidth": 70},
        {"headerName": "Value", "field": "Value", "flex": 1, "minWidth": 70},
        {"headerName": "BPS", "field": "BPS", "flex": 1, "minWidth": 70},    
    ]
    
    return df, col_defs

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
            'Expected Goals', 'Goals Scored', 'Total Points', 'BPS']
    
    df =  (
        player_database[player_database['Position'] == 'Forward'][cols]
        .sort_values(by='Total Points', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    col_defs = [
        {"headerName": "Name", "field": "Name", "flex": 2, "minWidth": 100, "pinned": "left", "cellStyle": {"font-weight": "bold", "text-transform": "uppercase"}},
        {"headerName": "Club", "field": "Club", "flex": 1, "minWidth": 100},
        {"headerName": "Price", "field": "Price", "flex": 1, "minWidth": 70},
        {"headerName": "Points", "field": "Total Points", "flex": 1, "minWidth": 70, "cellStyle": { "font-weight": "bold"}},
        {"headerName": "Starts", "field": "Starts", "flex": 1, "minWidth": 70},
        {"headerName": "xGI", "field": "Expected Goal Involvements", "flex": 1, "minWidth": 70},
        {"headerName": "Assists", "field": "Assists", "flex": 1, "minWidth": 70},
        {"headerName": "Goals", "field": "Goals Scored", "flex": 1, "minWidth": 70},
        {"headerName": "xG", "field": "Expected Goals", "flex": 1, "minWidth": 70},
        {"headerName": "SBP", "field": "Selected By (%)", "flex": 1, "minWidth": 70},
        {"headerName": "ICT", "field": "ICT Index", "flex": 1, "minWidth": 70},
        {"headerName": "ICT Rank", "field": "ICT Index Rank Type", "flex": 1, "minWidth": 70},
        {"headerName": "Form", "field": "Form", "flex": 1, "minWidth": 70},
        {"headerName": "Value", "field": "Value", "flex": 1, "minWidth": 70},
        {"headerName": "BPS", "field": "BPS", "flex": 1, "minWidth": 70},    
    ]
    
    return df, col_defs

def get_top_stats_for_player_cards(player_df):
    player_df = player_df.copy()
    cols_to_numeric = ['Total Points', 'Goals Scored', 'Assists', 'ICT Index', 'Clean Sheets', 'Defensive Contributions']
    player_df[cols_to_numeric] = player_df[cols_to_numeric].apply(pd.to_numeric, errors='coerce')
    most_points = player_df.nlargest(1, 'Total Points', keep='first') 
    most_goals = player_df.nlargest(1, 'Goals Scored', keep='first') 
    most_assists = player_df.nlargest(1, 'Assists', keep='first') 
    top_ict = player_df.nlargest(1, 'ICT Index', keep='first') 
    most_cleansheets = player_df.nlargest(1, 'Clean Sheets', keep='first') 
    most_defensive_contributions = player_df.nlargest(1, 'Defensive Contributions', keep='first') 
    return { 
            'Total Points' : most_points, 
            'Goals Scored' : most_goals, 
            'Assists' : most_assists, 
            'ICT Index' : top_ict, 
            'Clean Sheets' : most_cleansheets, 
            'Defensive Contributions' : most_defensive_contributions 
            }