# Operational Analytics Dashboard

A Python-based operational metrics pipeline that collects, processes, and visualizes delivery performance, error rates, and throughput data across distributed services. Built to enable data-driven decisions and proactive issue identification.

## Features

- Collects metrics from PostgreSQL and AWS CloudWatch
- Tracks delivery performance, error rates, throughput, and p99 latency
- Detects anomalies and triggers alerts when thresholds are breached
- Generates daily summary reports as JSON and CSV
- Lightweight dashboard served via Flask
- Scheduled via cron / AWS Lambda for automated reporting

## Tech Stack

- **Language:** Python 3.11
- **Database:** PostgreSQL
- **Cloud Metrics:** AWS CloudWatch
- **Web:** Flask
- **Data Processing:** pandas, psycopg2
- **Visualization:** matplotlib
- **Scheduling:** AWS Lambda / cron

## Project Structure

```
operational-analytics-dashboard/
├── src/
│   ├── collector.py        # Pulls metrics from PostgreSQL and CloudWatch
│   ├── processor.py        # Aggregates and computes KPIs
│   ├── anomaly.py          # Threshold-based anomaly detection
│   ├── report.py           # Generates JSON and CSV reports
│   └── app.py              # Flask dashboard server
├── tests/
│   ├── test_processor.py
│   └── test_anomaly.py
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/deepugi/operational-analytics-dashboard.git
cd operational-analytics-dashboard

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Set environment variables
export DB_HOST=localhost
export DB_NAME=analytics
export DB_USER=postgres
export DB_PASSWORD=your_password
export AWS_REGION=us-east-1
```

## Usage

```bash
# Run the metrics collection and processing pipeline
python src/collector.py

# Start the dashboard server
python src/app.py
# Open http://localhost:5000
```

## Running Tests

```bash
pytest tests/ -v
```

## License

MIT
