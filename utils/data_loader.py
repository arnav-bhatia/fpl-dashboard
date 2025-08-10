from typing import Tuple, Dict, List, Any
import requests

#Loading data from FPL API

def read_load_player_data(PLAYER_URL: str = "https://fantasy.premierleague.com/api/bootstrap-static/") -> Dict[str, Any]:
    """
    Loads player data from the FPL API and returns it in json format.

    Parameters:
        PLAYER_URL (string): URL of the API; Default value set.

    Returns:
        player_json (JSON): JSON file containing player data.

    Raises:
        RuntimeError: If there is an HTTP error or any other error during API call.
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

def read_load_fixtures_data(FIXTURES_URL: str = "https://fantasy.premierleague.com/api/fixtures/") -> Dict[str, Any]:
    """
    Loads fixture data from the FPL API and returns it in json format.

    Parameters:
        FIXTURES_URL (string): URL of the API; Default value set.

    Returns:
        fixtures_json (JSON): JSON file containing fixture data.

    Raises:
        RuntimeError: If there is an HTTP error or any other error during API call.
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

#Mapping dictionaries and lists

def get_pl_teams_dict_and_list(player_json: Dict[str, Any]) -> Tuple[Dict[int, str], List[str]]:
    """
    Returns all Premier League teams and their FPL ids.

    Parameters:
        player_json (JSON): JSON file from FPL API.

    Returns:
        pl_teams_dict (dict): Team ID to team name mapping.
        pl_teams_list (list): List of all team names.
    """
    pl_teams_dict: Dict[int, str] = {}
    pl_teams_list: List[str] = []
    for team in player_json["teams"]:
        pl_teams_dict[team["id"]] = team["name"]
        pl_teams_list.append(team["name"])
    return pl_teams_dict, pl_teams_list
    
def get_position_dict() -> Dict[int, str]:
    """
    Returns a dictionary containing the FPL position IDs as keys for the four positions.

    Parameters:
        None 

    Returns:
        position_dict (Dictionary): Dictionary containing the FPL position IDs as keys for the four positions.
    """
    position_dict = {1: "Goalkeeper", 
                     2: "Defender", 
                     3: "Midfielder", 
                     4: "Forward"}
    return position_dict

def get_status_dict() -> Dict[str, str]:
    """
    Returns a dictionary containing the FPL status IDs as keys for their different statuses.

    Parameters:
        None 

    Returns:
        position_dict (Dictionary): Dictionary containing the FPL status IDs as keys for their different statuses.
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