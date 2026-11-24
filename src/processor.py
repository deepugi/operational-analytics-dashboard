from typing import List, Dict


def compute_kpis(metrics: List[Dict]) -> Dict:
    """Compute high-level KPIs from collected delivery metrics."""
    if not metrics:
        return {}

    total = sum(r["total_deliveries"] for r in metrics)
    successful = sum(r["successful"] for r in metrics)
    failed = sum(r["failed"] for r in metrics)
    avg_ms = sum(r["avg_delivery_ms"] for r in metrics) / len(metrics)
    p99_values = [r["p99_ms"] for r in metrics if r["p99_ms"] is not None]
    p99_ms = max(p99_values) if p99_values else None

    success_rate = (successful / total * 100) if total > 0 else 0
    error_rate = (failed / total * 100) if total > 0 else 0

    return {
        "total_deliveries": total,
        "successful": successful,
        "failed": failed,
        "success_rate_pct": round(success_rate, 2),
        "error_rate_pct": round(error_rate, 2),
        "avg_delivery_ms": round(avg_ms, 2),
        "p99_delivery_ms": round(p99_ms, 2) if p99_ms else None,
    }


def compute_hourly_throughput(metrics: List[Dict]) -> List[Dict]:
    """Return per-hour throughput for trend analysis."""
    return [
        {
            "hour": str(r["hour"]),
            "throughput": r["total_deliveries"],
            "error_rate_pct": round(r["failed"] / r["total_deliveries"] * 100, 2)
            if r["total_deliveries"] > 0 else 0,
        }
        for r in metrics
    ]
