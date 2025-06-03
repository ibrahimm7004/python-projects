# Earthquake ETL Pipeline with Apache Airflow & Spark

---

## 📌 Objective

Build an end-to-end ETL pipeline using **Apache Airflow** and **Apache Spark** that:

- Ingests public earthquake data from a remote source
- Applies transformations using PySpark
- Stores the processed results in **Parquet** format on the local file system

---

## 🧱 Project Structure

etl_pipeline_project/
├── dags/
│ └── etl_pipeline.py # Airflow DAG with 3 sequential tasks
├── scripts/
│ ├── download_data.sh # Downloads earthquake data via curl
│ ├── transform_data.py # Performs Spark transformations
│ └── store_data.py # Converts CSV output to Parquet
├── data/
│ ├── earthquake_data.csv # Raw downloaded data
│ ├── temp_transformed/ # Intermediate CSVs
│ └── final_output.parquet # Final processed output
├── docker-compose.yaml # Airflow + Spark container config
└── README.md # This file

---

## 🌍 Dataset Used

- **Source**: USGS Earthquake Data Feed
- **URL**: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv
- **Format**: CSV
- **Description**: Contains global earthquakes from the past 30 days with fields such as time, magnitude, location, etc.

---

## 🔄 ETL Workflow Overview

### 1. Data Ingestion (`download_data`)

- Downloads the latest earthquake dataset using `curl`
- Saves it to `data/earthquake_data.csv`

### 2. Data Transformation (`transform_data`)

- Reads raw CSV with PySpark
- Applies the following transformations:
  - Filters out rows with missing or zero magnitude
  - Extracts `year` and `month` from timestamp
  - Aggregates average magnitude grouped by `year` and `month`
- Saves transformed data as CSV to `data/temp_transformed/`

### 3. Data Storage (`store_data`)

- Loads intermediate CSV output
- Writes the final transformed data to Parquet format at `data/final_output.parquet`

---

## 🚀 Running the Pipeline (via Docker Compose)

### 1. Start Airflow

```bash
docker-compose up airflow-init
docker-compose up -d

## 2. Access the Airflow UI

Open your browser and go to: [http://localhost:8080](http://localhost:8080)

Login with:
**Username**: `admin`
**Password**: `admin`

## 3. Trigger the DAG

- Enable the `earthquake_etl_pipeline` DAG
- Manually trigger a run via the UI

## 📂 Output Example (Parquet Data)

Example output from the Parquet file:

| year | month | average_magnitude |
|------|-------|-------------------|
| 2025 |   4   | 3.21              |
| 2025 |   5   | 2.87              |

## 🛠 Technologies Used

- Apache Airflow 2.8.1 (via Docker)
- Apache Spark (PySpark 3.5.0)
- Python 3.8
- Docker Compose
- curl

## 📦 Deliverables

- `dags/etl_pipeline.py` – Airflow DAG script
- `scripts/transform_data.py` – PySpark transformation
- `scripts/download_data.sh` – Ingestion script using curl
- `scripts/store_data.py` – CSV to Parquet converter
- `README.md` – Project documentation
- `notebook.ipynb` – Jupyter Notebook summary and outputs (submitted separately)

## 📝 Notes

- ETL logic is modular and can be reused or extended
- Each script is triggered independently via Airflow's BashOperator
- Data is stored locally under `data/` for easy inspection and reuse
```
