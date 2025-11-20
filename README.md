# NBP Currency Analytics Pipeline  
A complete end-to-end data engineering pipeline that fetches daily currency rates from the **NBP (National Bank of Poland) API**, processes them into a clean analytical dataset, stores them in a local **DuckDB warehouse**, backs them up to **AWS S3**, and exposes the data through:

- a **Streamlit dashboard**  
- analytical **SQL queries (DuckDB)**  
- GitHub Actions **automated daily ETL**

This project is structured and documented to serve as a **portfolio-grade Data Engineering case study**.

---

## 1. Project Architecture

```
NBP API → RAW JSON → Transform → Clean CSV → DuckDB Warehouse → S3 Backup → Dashboard / SQL Analysis
```

### Components:
- **Extract** – request daily tables (A/B) from the public NBP API  
- **Transform** – validation, schema standardization, timestamping  
- **Load** – incremental load into DuckDB  
- **Backup** – automatic upload of cleaned CSVs to AWS S3  
- **Analytics** – SQL views + Streamlit dashboard  
- **Automation** – GitHub Actions scheduled pipeline  

---

## 2. Repository Structure

```
pipeline1/
│
├── src/                         # ETL engine
│   ├── extract.py               # Fetching data from the NBP API
│   ├── transform.py             # Validation and data cleaning
│   ├── load.py                  # Loading processed data into DuckDB
│   ├── upload_to_s3.py          # Backup of processed CSV files to AWS S3
│   └── main.py                  # Main orchestrator (Extract → Transform → Load)
│
├── data/
│   ├── raw/                     # Raw JSON files from NBP API
│   ├── processed/               # Cleaned CSV files
│   └── local_datahub.duckdb     # Local DuckDB warehouse
│
├── dashboard/
│   └── dashboard.py             # Streamlit dashboard for visualization & analytics
│
├── sql/
│   ├── queries.sql              # Basic analytical SQL queries
│   └── analysis.sql             # Cross-currency and statistical analysis
│
├── .github/workflows/
│   └── nbp_pipeline.yml         # Automated ETL triggered on schedule or manually
│
├── config/
│   └── settings.py              # Configuration & environment variable management
│
├── requirements.txt
└── README.md
```

---

## 3. Installation & Setup

### 1. Clone the repository
```
git clone https://github.com/<your-user>/nbp-pipeline.git
cd nbp-pipeline
```

### 2. Create a virtual environment
```
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
.venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

---

## 4. Environment Variables (.env)

Create a `.env` file in the project root:

```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=your_bucket_name
AWS_S3_REGION=eu-central-1
```

---

## 5. Running the ETL Pipeline

### Full ETL run:
```
python src/main.py
```

This executes:

1. extract()  
2. transform()  
3. load()  
4. upload_to_s3()  

---

## 6. DuckDB: Local Analytics

Open the provided database:

```
duckdb data/local_datahub.duckdb
```

Example:

```
SELECT * FROM nbp_rates LIMIT 100;
```

---

## 7. Streamlit Dashboard

Launch:

```
streamlit run dashboard/dashboard.py
```

The dashboard provides:

- Daily rate trends  
- Cross-currency comparison  
- Volatility overview  
- Table views  
- Filtering by currency code  

---

## 8. SQL Analysis

### Basic preview
```sql
SELECT *
FROM nbp_rates
ORDER BY effective_date DESC
LIMIT 20;
```

### Currency trend
```sql
SELECT effective_date, mid
FROM nbp_rates
WHERE code = 'EUR'
ORDER BY effective_date;
```

### Summary statistics
```sql
SELECT
    code,
    MIN(mid) AS min_mid,
    MAX(mid) AS max_mid,
    AVG(mid) AS avg_mid,
    COUNT(*) AS obs_count
FROM nbp_rates
GROUP BY code
ORDER BY avg_mid DESC;
```

More queries are available in `sql/analysis.sql`.

---

## 9. GitHub Actions Automation

Daily run at 06:00 CET:

```
.github/workflows/nbp_pipeline.yml
```

Workflow includes:

- checkout  
- install dependencies  
- run ETL  
- upload cleaned data to S3  

Can also be executed manually via **workflow_dispatch**.

---

## 10. Why This Project Matters (Portfolio Value)

This repository demonstrates:

### ✔ Real ETL engineering  
You built a pipeline with clear stages, modular code, and reusable components.

### ✔ Cloud integration  
AWS S3 backup shows understanding of object storage workflows.

### ✔ Analytics-ready data modeling  
You created a usable analytical dataset in DuckDB.

### ✔ Visualization layer  
Dashboard proves end-to-end pipeline understanding.

### ✔ CI/CD / Automation  
Scheduled workflows in GitHub Actions are industry-standard.

### ✔ Clean architecture  
Professionally structured repository with configuration, SQL, ETL modules, and docs.

This is a **strong, real-world Data Engineering project** suitable for job applications, GitHub showcases, and CVs.

---

## 11. Future Extensions

- Add Airflow or Prefect orchestration  
- Add Great Expectations for data quality checks  
- Add dbt models for analytics  
- Add multi-table storage (rates, metadata, deltas)  
- Add monitoring (Prometheus + Grafana)  

---

## License

This project is distributed without a predefined license.  
You may add MIT for full open-source compatibility.

