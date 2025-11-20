# NBP Daily Currency Pipeline
Kompletny projekt ETL → Warehouse (DuckDB) → Dashboard → S3 → GitHub Actions

Projekt pobiera codziennie kursy walut z API NBP, przetwarza je, odkłada w lokalnym magazynie danych DuckDB, generuje czyste dataset CSV i wysyła kopię do AWS S3. Następnie dane analizowane są poprzez zestaw SQL oraz interaktywny dashboard oparty o Streamlit.

Całość działa automatycznie dzięki GitHub Actions, a kod jest modularny, czytelny i gotowy do rozszerzeń.

## Architektura projektu

NBP API → RAW JSON → Transform → Clean CSV → DuckDB Warehouse → S3 Backup → Dashboard / SQL Analysis

## Struktura repozytorium

pipeline1/
│
├── src/                 # Silnik ETL
│   ├── extract.py       # Pobranie danych z API NBP
│   ├── transform.py     # Walidacja i czyszczenie danych
│   ├── load.py          # Załadunek do DuckDB
│   ├── upload_to_s3.py  # Backup CSV do AWS S3
│   └── main.py          # Główny orchestrator
│
├── data/
│   ├── raw/             # Surowe dane JSON
│   ├── processed/       # Oczyszczone CSV
│   └── local_datahub.duckdb
│
├── dashboard/
│   └── dashboard.py     # Streamlit – analizy i wizualizacje
│
├── sql/
│   ├── queries.sql
│   └── analysis.sql     # Kompletny zestaw analiz międzywalutowych
│
├── .github/workflows/
│   └── nbp_pipeline.yml # Automatyzacja ETL w GitHub Actions
│
├── config/settings.py   # Zarządzanie konfiguracją i zmiennymi środowiskowymi
├── requirements.txt
└── README.md

## Instalacja i uruchamianie

### 1. Klonowanie repozytorium

git clone <repo_url>
cd pipeline1

### 2. Instalacja zależności

pip install -r requirements.txt

### 3. Uruchomienie lokalnego ETL

python src/main.py

### 4. Uruchomienie dashboardu

streamlit run dashboard/dashboard.py

Dashboard automatycznie pobierze dane z lokalnej bazy DuckDB.

## Automatyzacja: GitHub Actions

Pipeline działa raz dziennie dzięki definicji:

.github/workflows/nbp_pipeline.yml

Wykonuje:
1. Pobranie repo
2. Instalację środowiska
3. Uruchomienie ETL
4. Przetwarzanie CSV
5. Upload do S3
6. Logowanie i raportowanie

Dzięki temu projekt może działać nieprzerwanie bez udziału użytkownika.

## Dashboard (Streamlit)

Dashboard składa się z kilku sekcji:

- Trend kursu wybranej waluty  
- Dzienne zmiany procentowe  
- Analiza zmienności  
- Porównania międzywalutowe  
- Heatmapa korelacji  
- Ranking walut  

Dashboard czyta dane z DuckDB, co zapewnia wysoką wydajność i prostą integrację.

## Analizy SQL

Pełny zestaw zapytań znajduje się w:

sql/analysis.sql

Zawiera:
- zmiany dzień do dnia  
- ranking zmienności  
- porównania dwóch walut  
- korelacje  
- ranking walut po średnim kursie  
- top wzrosty w czasie  
- heatmapę korelacji  

## Konfiguracja AWS

Zmienne środowiskowe:

AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>
AWS_DEFAULT_REGION=<region>
AWS_BUCKET_NAME=<bucket>

Pipeline automatycznie wysyła pliki:

data/processed/*.csv

do S3 w strukturze:

s3://bucket/data/processed/YYYY-MM-DD.csv

## Logowanie

Pełny log działania dostępny jest w:

logs/pipeline.log

## Dlaczego DuckDB?

DuckDB pełni rolę lokalnego magazynu danych:
- zero konfiguracji
- wysokie osiągi w analityce kolumnowej
- łatwa integracja z Pythonem i dashboardami
- idealne do projektów portfolio

## Możliwe rozszerzenia

- metadata tracking ETL  
- walidacja danych (schema enforcement)  
- automatyczne raporty PDF  
- integracja z Snowflake lub BigQuery  
- wdrożenie dashboardu online (Streamlit Cloud)

## Licencja

Projekt do celów edukacyjnych i demonstracyjnych.
