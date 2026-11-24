from typing import Dict, List


DEFAULT_THRESHOLDS = {
    "error_rate_pct": 5.0,       # Alert if error rate exceeds 5%
    "p99_delivery_ms": 3000,     # Alert if p99 latency exceeds 3 seconds
    "avg_delivery_ms": 1000,     # Alert if avg latency exceeds 1 second
}


def detect_anomalies(kpis: Dict, thresholds: Dict = None) -> List[Dict]:
    """
    Compare KPIs against thresholds and return a list of anomalies.
    Each anomaly has: metric, value, threshold, severity.
    """
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    anomalies = []

    for metric, threshold in thresholds.items():
        value = kpis.get(metric)
        if value is None:
            continue

        if value > threshold:
            severity = "critical" if value > threshold * 1.5 else "warning"
            anomalies.append({
                "metric": metric,
                "value": value,
                "threshold": threshold,
                "severity": severity,
                "message": f"{metric} is {value} (threshold: {threshold})"
            })

    return anomalies
