import sys
from .extract import extract_nbp_data
from .transform import transform_nbp_data
from .load import load_to_duckdb
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logging.info("=== PIPELINE START ===")
    try:
        extract_nbp_data()
        transform_nbp_data()
        load_to_duckdb()
    except Exception as e:
        logging.exception(f"Pipeline failed with error: {e}")
        sys.exit(1)
    else:
        logging.info("=== PIPELINE END (SUCCESS) ===")
        sys.exit(0)