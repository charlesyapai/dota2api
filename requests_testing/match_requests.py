"""This script:
1. Loads a match ID from a YAML configuration file.
2. Fetches match data from the OpenDota API using that match ID.
3. Saves the retrieved match data to a YAML file named after the match ID.

The script logs each step, rather than printing large amounts of data.
"""  # noqa: INP001

import logging
import os

import requests
import yaml

# =============================================================================
# Configuration Section
# =============================================================================
# Adjust these paths and settings as needed.
CONFIG_YAML_PATH = "requests_testing/configurations.yaml"
OUTPUT_DIR = "requests_testing/data/matches"
LOG_LEVEL = logging.DEBUG

# Set up logging configuration
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# =============
# Main Function
# =============

def main():
    """Main execution flow:
    1. Load the match ID from the YAML file defined in CONFIG_YAML_PATH.
    2. Retrieve match data from the OpenDota API.
    3. Save the data to a YAML file named after the match ID.
    """
    match_id = load_match_id_from_yaml(CONFIG_YAML_PATH)
    match_data = get_match_data(match_id)
    save_match_data_to_yaml(match_id, match_data, OUTPUT_DIR)

# =============
# Supporting Functions
# =============

def load_match_id_from_yaml(file_path: str) -> int:
    """Load the match ID from a given YAML file.

    The YAML file should contain:
    match_id_test: <integer>

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        int: The match ID extracted from the YAML file.

    Raises:
        ValueError: If 'match_id_test' is not found or the file is invalid.

    """
    logging.info(f"Loading match_id from YAML file: {file_path}")
    with open(file_path, encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not data or "match_id_test" not in data:
        logging.error("No 'match_id_test' key found in the provided YAML file.")
        msg = f"No 'match_id_test' key found in {file_path}."
        raise ValueError(msg)

    match_id = data["match_id_test"]
    logging.debug(f"Loaded match_id: {match_id}")
    return match_id


def get_match_data(match_id: int) -> dict:
    """Fetch match data from the OpenDota API for the given match ID.

    Args:
        match_id (int): The match ID to retrieve data for.

    Returns:
        dict: The match data as a dictionary.

    Raises:
        requests.HTTPError: If the HTTP request fails.
    """
    logging.info(f"Fetching match data from OpenDota API for match_id: {match_id}")
    url = f"https://api.opendota.com/api/matches/{match_id}"
    response = requests.get(url)
    response.raise_for_status()
    logging.debug("Match data successfully retrieved from the API.")
    return response.json()


def save_match_data_to_yaml(match_id: int, match_data: dict, output_dir: str):
    """Save the retrieved match data to a YAML file named after the match ID.

    Args:
        match_id (int): The match ID to use for the filename.
        match_data (dict): The match data dictionary to save.
        output_dir (str): The directory where the YAML file will be stored.
    """
    if not os.path.exists(output_dir):
        logging.debug(f"Output directory does not exist, creating: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"match-{match_id}.yaml")
    logging.info(f"Saving match data to {filename}")
    with open(filename, "w", encoding="utf-8") as f:
        yaml.safe_dump(match_data, f)
    logging.debug("Match data successfully saved.")




if __name__ == "__main__":
    main()
