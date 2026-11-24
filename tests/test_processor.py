from src.processor import compute_kpis, compute_hourly_throughput
from datetime import datetime


def _sample_metrics():
    return [
        {"hour": datetime(2024, 1, 1, 10), "total_deliveries": 1000, "successful": 950, "failed": 50, "avg_delivery_ms": 200, "p99_ms": 800},
        {"hour": datetime(2024, 1, 1, 11), "total_deliveries": 1200, "successful": 1180, "failed": 20, "avg_delivery_ms": 180, "p99_ms": 750},
    ]


def test_compute_kpis_success_rate():
    kpis = compute_kpis(_sample_metrics())
    assert kpis["total_deliveries"] == 2200
    assert kpis["successful"] == 2130
    assert kpis["failed"] == 70
    assert kpis["success_rate_pct"] == round(2130 / 2200 * 100, 2)


def test_compute_kpis_empty():
    kpis = compute_kpis([])
    assert kpis == {}


def test_hourly_throughput_shape():
    hourly = compute_hourly_throughput(_sample_metrics())
    assert len(hourly) == 2
    assert "throughput" in hourly[0]
    assert "error_rate_pct" in hourly[0]
