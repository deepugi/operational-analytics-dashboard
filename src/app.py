from flask import Flask, jsonify
from collector import collect_delivery_metrics
from processor import compute_kpis, compute_hourly_throughput
from anomaly import detect_anomalies

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/kpis")
def kpis():
    metrics = collect_delivery_metrics(hours=24)
    kpi_data = compute_kpis(metrics)
    anomalies = detect_anomalies(kpi_data)
    return jsonify({
        "kpis": kpi_data,
        "anomalies": anomalies,
        "anomaly_count": len(anomalies)
    })


@app.route("/api/throughput")
def throughput():
    metrics = collect_delivery_metrics(hours=24)
    hourly = compute_hourly_throughput(metrics)
    return jsonify({"hourly_throughput": hourly})


@app.route("/api/summary")
def summary():
    metrics = collect_delivery_metrics(hours=24)
    kpi_data = compute_kpis(metrics)
    hourly = compute_hourly_throughput(metrics)
    anomalies = detect_anomalies(kpi_data)
    return jsonify({
        "kpis": kpi_data,
        "hourly_throughput": hourly,
        "anomalies": anomalies
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
