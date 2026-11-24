from src.anomaly import detect_anomalies


def test_no_anomalies_when_within_threshold():
    kpis = {"error_rate_pct": 2.0, "p99_delivery_ms": 500, "avg_delivery_ms": 300}
    anomalies = detect_anomalies(kpis)
    assert len(anomalies) == 0


def test_detects_high_error_rate():
    kpis = {"error_rate_pct": 10.0, "p99_delivery_ms": 500, "avg_delivery_ms": 300}
    anomalies = detect_anomalies(kpis)
    assert any(a["metric"] == "error_rate_pct" for a in anomalies)


def test_critical_severity_when_double_threshold():
    kpis = {"error_rate_pct": 20.0}
    anomalies = detect_anomalies(kpis, thresholds={"error_rate_pct": 5.0})
    assert anomalies[0]["severity"] == "critical"


def test_warning_severity_just_above_threshold():
    kpis = {"error_rate_pct": 6.0}
    anomalies = detect_anomalies(kpis, thresholds={"error_rate_pct": 5.0})
    assert anomalies[0]["severity"] == "warning"
