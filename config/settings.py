"""
settings.py
-----------
Loads environment variables from the .env file and makes them available
as class attributes via Settings.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Locate and load .env from the project root (pipeline1/.env)
BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    print(f"⚠️  Warning: .env file not found at {ENV_PATH}")

class Settings:
    # AWS credentials
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "eu-central-1")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    # Local paths
    DUCKDB_PATH = os.getenv("DUCKDB_PATH", "data/local_datahub.duckdb")
    LOG_PATH = os.getenv("LOG_PATH", "logs/pipeline.log")
