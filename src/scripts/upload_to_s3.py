"""
upload_to_s3.py
---------------
Uploads a file (e.g. processed CSV) to an AWS S3 bucket.
Reads credentials and bucket name from environment variables (.env).
"""

import os
import logging
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from config.settings import Settings  # loads env vars

# --- Setup logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(Settings.LOG_PATH),
        logging.StreamHandler()
    ]
)

def upload_csv_to_s3(local_path: str, s3_subdir: str = "data/processed/") -> bool:
    """
    Uploads a local CSV file to AWS S3 bucket.
    """

    try:
        file_path = Path(local_path)
        if not file_path.exists():
            logging.error(f"❌ File not found: {file_path}")
            return False

        # --- Validate required AWS envs ---
        required_envs = [
            Settings.AWS_ACCESS_KEY_ID,
            Settings.AWS_SECRET_ACCESS_KEY,
            Settings.AWS_DEFAULT_REGION,
            Settings.AWS_BUCKET_NAME,
        ]
        if not all(required_envs):
            logging.error("❌ Missing AWS credentials or configuration — skipping S3 upload.")
            return False

        # --- Initialize S3 resource ---
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_DEFAULT_REGION
        )

        bucket = s3.Bucket(Settings.AWS_BUCKET_NAME)
        s3_key = f"{s3_subdir}{file_path.name}"

        logging.info(f"Uploading {file_path.name} to s3://{Settings.AWS_BUCKET_NAME}/{s3_key} ...")

        bucket.upload_file(
            str(file_path),
            s3_key,
            ExtraArgs={"ContentType": "text/csv"}
        )

        logging.info(f"✅ Uploaded {file_path.name} successfully.")
        return True

    except ClientError as e:
        logging.exception(f"AWS ClientError: {e}")
        return False
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    # Manual test:
    TEST_FILE = "data/processed/nbp_rates_2025-10-22.csv"
    upload_csv_to_s3(TEST_FILE)
