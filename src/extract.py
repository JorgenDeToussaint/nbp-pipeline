import requests
import json
import os
from datetime import datetime
import logging
from pathlib import Path


# --- Directory setup ---
BASE_DIR = Path(__file__).resolve().parents[1]  # src -> pipeline1
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging On GitHub Actions, logs are better viewed in the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()  # prints also to console
    ]
)

# --- Configure logging ---
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / "pipeline.log",
    level=logging.INFO
)

# --- Endpoint ---
URL = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"

def extract_nbp_data():
    """
    Fetches daily exchange rates from NBP API and saves to data/raw_nbp_<date>.json
    """
    try:
        logging.info(f"Fetching data from {URL}")
        response = requests.get(URL, timeout=10)
        if response.status_code !=200:
            raise ValueError(f"NBP API returned unexpected status: {response.status_code}")
        response.raise_for_status()

        data = response.json()
        if not data or "rates" not in data[0]:
            raise ValueError("Invalid NBP API structure — missing 'rates' key")
        filename = DATA_DIR / f"raw_nbp_{datetime.now().date()}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logging.info(f"Fetched {len(data[0]['rates'])} currency records.")
        
        logging.info(f"Data successfully saved to {filename}")
        print(f"✅ Data saved: {filename}")

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error while fetching data: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    extract_nbp_data()