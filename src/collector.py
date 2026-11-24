import os
import boto3
import psycopg2
from datetime import datetime, timedelta


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "analytics"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )


def collect_delivery_metrics(hours: int = 24) -> list:
    """Pull delivery performance metrics from PostgreSQL."""
    conn = get_db_connection()
    since = datetime.utcnow() - timedelta(hours=hours)

    query = """
        SELECT
            DATE_TRUNC('hour', created_at) AS hour,
            COUNT(*) AS total_deliveries,
            SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS successful,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed,
            AVG(delivery_time_ms) AS avg_delivery_ms,
            PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY delivery_time_ms) AS p99_ms
        FROM deliveries
        WHERE created_at >= %s
        GROUP BY DATE_TRUNC('hour', created_at)
        ORDER BY hour ASC;
    """

    with conn.cursor() as cur:
        cur.execute(query, (since,))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

    conn.close()
    return [dict(zip(columns, row)) for row in rows]


def collect_cloudwatch_metrics(metric_name: str, namespace: str, hours: int = 24) -> list:
    """Pull metrics from AWS CloudWatch."""
    client = boto3.client("cloudwatch", region_name=os.getenv("AWS_REGION", "us-east-1"))
    end = datetime.utcnow()
    start = end - timedelta(hours=hours)

    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start,
        EndTime=end,
        Period=3600,
        Statistics=["Average", "Sum", "Maximum"],
    )

    datapoints = sorted(response["Datapoints"], key=lambda x: x["Timestamp"])
    return datapoints
