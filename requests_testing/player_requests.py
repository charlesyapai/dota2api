"""This script:
1. Loads a player ID from a YAML configuration file.
2. Fetches multiple sets of player data from the OpenDota API.
3. Saves each set of retrieved data into separate YAML files under a folder named after the player ID.
4. Continues running even if one or more endpoints fail, logging errors instead of stopping the script.
5. Outputs a final dictionary of sections and their statuses (e.g., success, retrieval_failed, save_failed).

We've integrated `rich` to provide colored and enhanced output in the terminal.

Prerequisites:
- Python 3.x
- requests: `pip install requests`
- pyyaml: `pip install pyyaml`
- rich: `pip install rich`

File Structure:
- configurations.yaml (contains `player_id_test`)
- This script (e.g., player_additional_data_request.py)
"""

import logging
import os

import requests
import yaml
from rich.console import Console
from rich.logging import RichHandler

# =============================================================================
# Configuration Section
# =============================================================================
CONFIG_YAML_PATH = "requests_testing/configurations.yaml"
OUTPUT_DIR = "requests_testing/data/players"
LOG_LEVEL = logging.DEBUG

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)
logger = logging.getLogger(__name__)
console = Console()


# =============
# Main Function
# =============


def main() -> None:
    """Main execution flow:
    1. Load the player ID from the YAML file defined in CONFIG_YAML_PATH.
    2. Create a directory based on the player ID.
    3. Fetch data from each specified endpoint and save each to a separate YAML file if retrieval succeeds.
    4. Perform a POST to refresh the player data and save the response if successful.
    5. Output a final dictionary showing the status of each section.
    """
    logger.info("[bold cyan]Starting player data retrieval process...[/bold cyan]")
    # Loading configurations
    enpoints_config = load_config(CONFIG_YAML_PATH)["endpoints"]
    player_id = load_player_id_from_yaml(CONFIG_YAML_PATH)

    player_dir = os.path.join(OUTPUT_DIR, str(player_id))
    logger.info(f"Data will be saved under: [bold yellow]{player_dir}[/bold yellow]")

    base_url = f"https://api.opendota.com/api/players/{player_id}"


    # Endpoints available by OpenDota API for player data
    endpoints = {
        "player": (f"{base_url}", "general player data"),
        "wl": (f"{base_url}/wl", "win/loss data"),
        "recentMatches": (f"{base_url}/recentMatches", "recent matches data"),
        "matches": (f"{base_url}/matches", "all matches data"),
        "heroes": (f"{base_url}/heroes", "heroes data"),
        "peers": (f"{base_url}/peers", "peers data"),
        "pros": (f"{base_url}/pros", "pros data"),
        "totals": (f"{base_url}/totals", "totals data"),
        "counts": (f"{base_url}/counts", "counts data"),
        "histograms": (f"{base_url}/histograms", "histograms data"),
        "wardmap": (f"{base_url}/wardmap", "wardmap data"),
        "wordcloud": (f"{base_url}/wordcloud", "wordcloud data"),
        "ratings": (f"{base_url}/ratings", "ratings data"),
        "rankings": (f"{base_url}/rankings", "rankings data"),
    }

    # Based on endpoints_config, create a new active_endpoints dictionary
    active_endpoints = {key: value for key, value in endpoints.items() if enpoints_config.get(key, False)}
    logger.info(f"Active endpoints: {active_endpoints.keys()}")

    # Results dictionary to store the status of each section
    results = {}

    # Fetch and save GET endpoints
    for filename, (url, desc) in active_endpoints.items():
        logger.info(f"Attempting to retrieve [magenta]{desc}[/magenta]...")
        data = fetch_data_from_endpoint(url, desc)
        if data is not None:
            logger.info(f"[green]Successfully retrieved[/green] {desc}. Now saving...")
            save_success = save_data_to_yaml(data, player_dir, f"{filename}.yaml", desc)
            if save_success:
                results[filename] = "success"
            else:
                results[filename] = "save_failed"
        else:
            logger.warning(f"[yellow]Skipping saving {desc} due to retrieval failure.[/yellow]")
            results[filename] = "retrieval_failed"

    # Attempt POST to refresh endpoint and save the response
    refresh_url = f"{base_url}/refresh"
    logger.info("Attempting to [magenta]refresh player data[/magenta]...")
    refresh_data = post_data_to_endpoint(refresh_url, "player refresh")
    if refresh_data is not None:
        logger.info("[green]Successfully refreshed[/green] player data. Now saving...")
        save_success = save_data_to_yaml(refresh_data, player_dir, "refresh.yaml", "refresh data")
        if save_success:
            results["refresh"] = "success"
        else:
            results["refresh"] = "save_failed"
    else:
        logger.warning("[yellow]Skipping saving refresh data due to retrieval failure.[/yellow]")
        results["refresh"] = "retrieval_failed"

    logger.info("[bold cyan]Data fetching process completed.[/bold cyan]")
    logger.info("Final Results:")
    for section, status in results.items():
        color = "green" if status == "success" else "red" if status == "save_failed" else "yellow"
        logger.info(f"[{color}]{section}: {status}[/{color}]")

    console.print("\n[bold underline magenta]Final Results Dictionary:[/bold underline magenta]", results)




# =============================================================================
# Supporting Functions
# =============================================================================

def load_config(file_path: str) -> dict:
    """Load a YAML configuration file."""
    with open(file_path, encoding="utf-8") as file:
        return yaml.safe_load(file)

def load_player_id_from_yaml(file_path: str) -> int:
    """
    Load the player ID from a given YAML file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        int: The player ID extracted from the YAML file.
    """
    logger.info(f"Loading player_id from YAML file: [bold yellow]{file_path}[/bold yellow]")
    if not os.path.isfile(file_path):
        logger.error(f"[red]The file {file_path} does not exist.[/red]")
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not data or "player_id_test" not in data:
        logger.error("[red]No 'player_id_test' key found in the provided YAML file.[/red]")
        raise ValueError(f"No 'player_id_test' key found in {file_path}.")

    player_id = data["player_id_test"]
    if not isinstance(player_id, int):
        logger.error(f"[red]player_id_test should be an integer, got {type(player_id)} instead.[/red]")
        raise ValueError("player_id_test value must be an integer.")

    logger.debug(f"Loaded player_id: {player_id}")
    return player_id


def fetch_data_from_endpoint(url: str, description: str) -> dict or list or None:
    """Fetch data from a given endpoint and return the JSON response.

    Args:
        url (str): The URL of the endpoint to fetch data from.
        description (str): A description of the data being fetched.

    Returns:
        dict or list or None: The JSON response data retrieved from the endpoint.

    Raises:
        requests.HTTPError: If there is an HTTP error while fetching the data.

    """
    logger.debug(f"Fetching {description} from endpoint: {url}")
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.exception(f"[red]Failed to fetch {description} data: {e}[/red]")
        return None

    data = response.json()
    logger.debug(f"{description} retrieved successfully. Type: {type(data)}")
    return data


def post_data_to_endpoint(url: str, description: str) -> dict or list or None:
    logger.debug(f"Posting to {description} endpoint: {url}")
    response = requests.post(url)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.exception(f"[red]Failed to POST {description}: {e}[/red]")
        return None

    data = response.json()
    logger.debug(f"POST {description} succeeded. Type: {type(data)}")
    return data


def save_data_to_yaml(data: dict or list, directory: str, filename: str, description: str) -> bool:
    """Save data to a YAML file. Used in the main function to save retrieved data.

    Args:
        data (dict or list): The data to save.
        directory (str): The directory to save the file in.
        filename (str): The filename to save the data as.
        description (str): A description of the data being saved.
    """
    if not os.path.exists(directory):
        logger.debug(f"Output directory does not exist, creating: {directory}")
        os.makedirs(directory, exist_ok=True)

    filepath = os.path.join(directory, filename)
    logger.debug(f"Saving {description} to {filepath}")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f)
        logger.info(f"[green]{description.capitalize()} successfully saved[/green] to {filepath}")
        return True
    except OSError as e:
        logger.error(f"[red]Failed to write {description} to {filepath}: {e}[/red]")
        return False


if __name__ == "__main__":
    main()
