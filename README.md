This repository is for experimenting with interacting with the Dota 2 API, focusing on retrieving information about:

1. Past Matches
- Pulling up detailed stats about a single tournament
- Summarizing match information

2. Live Matches
- Being able to utilize the information being fed directly.


# OpenDota Data Pipeline Project

This project is designed to interact with the OpenDota API to generate statistics, clean data, perform data analysis, and train models to learn patterns about players, matches, and heroes. The project is organized into several sections, each representing a different stage of the data pipeline.

## Project Structure

```sh
    project_root/
    │
    ├── configs/
    │   └── configurations.yaml
    │
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   └── models/
    │
    ├── src/
    │   ├── utils/
    │   │   └── player_requests.py
    │   │   └── data_processing.py
    │   │   └── api_interaction.py
    │   │   └── logging_setup.py
    │   │   └── config_loader.py
    │   │
    │   ├── scraping/
    │   │   └── fetch_player_data.py
    │   │   └── fetch_match_data.py
    │   │
    │   ├── cleaning/
    │   │   └── clean_player_data.py
    │   │   └── clean_match_data.py
    │   │
    │   ├── analysis/
    │   │   └── analyze_player_stats.py
    │   │   └── analyze_match_stats.py
    │   │
    │   ├── modeling/
    │   │   └── train_model.py
    │   │   └── evaluate_model.py
    │   │   └── infer_model.py
    │   │
    │   └── pipelines/
    │       └── data_pipeline.py
    │       └── analysis_pipeline.py
    │       └── modeling_pipeline.py
    │
    ├── tests/
    │   ├── test_utils/
    │   ├── test_scraping/
    │   ├── test_cleaning/
    │   ├── test_analysis/
    │   └── test_modeling/
    │
    ├── notebooks/
    │   └── exploratory_data_analysis.ipynb
    │   └── model_training.ipynb
    │
    ├── requirements.txt
    ├── README.md
    └── setup.py
```


## Directory Descriptions

- **configs/**: Contains configuration files like `configurations.yaml`.
- **data/**: Organizes data files:
  - `raw/`: Raw data fetched from the API.
  - `processed/`: Cleaned and processed data ready for analysis.
  - `models/`: Trained models and related files.
- **src/**: Main source code directory:
  - `utils/`: Utility scripts for common tasks (e.g., API interaction, data processing, logging setup).
  - `scraping/`: Scripts for data scraping from the OpenDota API.
  - `cleaning/`: Scripts for cleaning and preprocessing data.
  - `analysis/`: Scripts for data analysis.
  - `modeling/`: Scripts for model training, evaluation, and inference.
  - `pipelines/`: Scripts that define end-to-end pipelines for data processing, analysis, and modeling.
- **tests/**: Unit tests for different modules:
  - `test_utils/`: Tests for utility functions.
  - `test_scraping/`: Tests for scraping scripts.
  - `test_cleaning/`: Tests for cleaning scripts.
  - `test_analysis/`: Tests for analysis scripts.
  - `test_modeling/`: Tests for modeling scripts.
- **notebooks/**: Jupyter notebooks for exploratory data analysis and model training.
- **requirements.txt**: List of dependencies.
- **README.md**: Project documentation.
- **setup.py**: Script for setting up the project as a package.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/opendota-data-pipeline.git
cd opendota-data-pipeline
```

2. Install the required packages:
```sh
pip install -r requirements.txt
```

###  Configuration
Update the configs/configurations.yaml file with your OpenDota API key and other necessary configurations.

### Running the Pipelines

#### Data Scraping
To fetch player data from the OpenDota API:

```sh
python src/scraping/fetch_player_data.py <player_id>
```

#### Data Cleaning
To clean the fetched player data:

```sh
python src/cleaning/clean_player_data.py
```

#### Data Analysis
To analyze player statistics:

```sh
python src/analysis/analyze_player_stats.py
```


#### Model Training
To train a model:

```sh
python src/modeling/train_model.py
```

#### Running Tests
To run the tests:

```sh
pytest tests/
```

#### Using Jupyter Notebooks
To explore data and train models using Jupyter notebooks:

```sh
jupyter notebook notebooks/exploratory_data_analysis.ipynb
```


### Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contact
For any questions or suggestions, please open an issue or contact the project maintainer.