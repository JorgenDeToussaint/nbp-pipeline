import logging
from pathlib import Path
import duckdb
import pandas as pd

# Ścieżki
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
DB_PATH = DATA_DIR / "local_datahub.duckdb"
PROCESSED_DIR = DATA_DIR / "processed"

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

def load_to_duckdb():
    """Ładuje wszystkie pliki CSV z processed/ do DuckDB, nadpisując istniejące daty."""
    try:
        processed_files = sorted(PROCESSED_DIR.glob("nbp_rates_*.csv"))
        if not processed_files:
            raise FileNotFoundError("Brak plików CSV w folderze processed/")

        conn = duckdb.connect(str(DB_PATH))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS nbp_rates (
                currency VARCHAR,
                code VARCHAR,
                mid DOUBLE,
                table_name VARCHAR,
                effective_date DATE,
                transform_timestamp TIMESTAMP
            )
        """)

        for file in processed_files:
            logging.info(f"Ładowanie: {file.name}")
            df = pd.read_csv(file)

            if "effectiveDate" in df.columns:
                df.rename(columns={"effectiveDate": "effective_date"}, inplace=True)

            for d in df["effective_date"].unique():
                conn.execute("DELETE FROM nbp_rates WHERE effective_date = ?", [d])

            conn.execute("INSERT INTO nbp_rates SELECT * FROM df")
            logging.info(f"Wczytano {len(df)} rekordów z {file.name}")

        conn.close()
        logging.info("Załadowano wszystkie pliki do DuckDB.")

        # --- Upload to AWS S3 after successful load ---
        try:
            from src.scripts.upload_to_s3 import upload_csv_to_s3
            upload_success = upload_csv_to_s3(str(file))
            if upload_success:
                logging.info(f"✅ Uploaded {file.name} to S3 successfully.")
            else:
                logging.warning(f"⚠️ Upload to S3 failed for {file.name}.")
        except Exception as e:
                logging.exception(f"❌ S3 upload step failed for {file.name}: {e}")


    except Exception as e:
        logging.error(f"Błąd ładowania danych: {e}")
        print(f"Błąd: {e}")

if __name__ == "__main__":
    load_to_duckdb()
