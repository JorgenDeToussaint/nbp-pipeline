import json
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

# --- Directory setup ---
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
PROCESSED_DIR = DATA_DIR / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

def transform_nbp_data():
    """
    Reads the latest raw NBP JSON, flattens into DF, adds timestamp, and saves as clean CSV.
    """
    try:
        raw_files = sorted(DATA_DIR.glob("raw_nbp_*.json"), reverse=True)
        if not raw_files:
            raise FileNotFoundError("No raw NBP data files found.")
        latest_file = raw_files[0]
        logging.info(f"Transforming data from {latest_file}")

        with open(latest_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        rates = data[0]["rates"]
        df = pd.DataFrame(rates)

        # 🧩 1️⃣ Usuń ewentualną kolumnę 'table' po rename, jeśli istnieje
        df.rename(columns={"table": "table_name"}, inplace=True)
        if "table" in df.columns:
            df.drop(columns=["table"], inplace=True)

        # 🧩 2️⃣ Konwersja i kolumny dodatkowe
        df["mid"] = pd.to_numeric(df["mid"], errors="coerce")
        df.dropna(subset=["mid"], inplace=True)
        df["table"] = data[0]["table"]
        df["effectiveDate"] = data[0]["effectiveDate"]
        df["transform_timestamp"] = datetime.now().isoformat(timespec="seconds")

        # 🧩 3️⃣ Łagodna walidacja kolumn
        expected_cols = {"currency", "code", "mid", "table_name", "effectiveDate", "transform_timestamp"}
        missing = expected_cols - set(df.columns)
        extra = set(df.columns) - expected_cols
        if missing:
            logging.warning(f"Missing expected columns: {missing}")
        if extra:
            logging.warning(f"Extra columns detected: {extra}")

        # --- Save file ---
        processed_file = PROCESSED_DIR / f"nbp_rates_{datetime.now().date()}.csv"
        df.to_csv(processed_file, index=False, encoding="utf-8-sig")

        logging.info(f"Transformed data saved to {processed_file}")
        print(f"✅ Data transformed and saved: {processed_file}")

    except Exception as e:
        logging.error(f"File error: {e}")
        print(f"❌ Error during transformation: {e}")

    
if __name__ == "__main__":
    transform_nbp_data()