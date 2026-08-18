"""
API Performance Tests
Requirements: Section 18 - Performance Validation
"""

import time
import statistics


# Snowflake-backed API calls can take longer than a local in-memory API.
# 5 seconds is used as the maximum acceptable individual request latency.
MAX_LATENCY_MS = 5000


def measure_request(api_client, method, endpoint, **kwargs):
    """Measure API request latency in milliseconds."""

    start = time.perf_counter()

    response = getattr(api_client, method)(
        endpoint,
        **kwargs
    )

    elapsed_ms = (time.perf_counter() - start) * 1000

    return response, elapsed_ms


def test_health_latency(api_client):
    """Health endpoint should respond within 5 seconds."""

    response, elapsed_ms = measure_request(
        api_client,
        "get",
        "/health"
    )

    assert response.status_code == 200

    assert elapsed_ms < MAX_LATENCY_MS, (
        f"Health response time {elapsed_ms:.2f}ms "
        f"exceeds {MAX_LATENCY_MS}ms threshold"
    )


def test_get_portfolio_latency(api_client):
    """Get portfolio endpoint should respond within 5 seconds."""

    response, elapsed_ms = measure_request(
        api_client,
        "get",
        "/portfolios/P10001"
    )

    assert response.status_code == 200

    assert elapsed_ms < MAX_LATENCY_MS, (
        f"Portfolio response time {elapsed_ms:.2f}ms "
        f"exceeds {MAX_LATENCY_MS}ms threshold"
    )


def test_list_portfolios_latency(api_client):
    """Portfolio listing should respond within 5 seconds."""

    response, elapsed_ms = measure_request(
        api_client,
        "get",
        "/portfolios"
    )

    assert response.status_code == 200

    assert elapsed_ms < MAX_LATENCY_MS, (
        f"Portfolio list response time {elapsed_ms:.2f}ms "
        f"exceeds {MAX_LATENCY_MS}ms threshold"
    )


def test_holdings_latency(api_client):
    """Holdings endpoint should respond within 5 seconds."""

    response, elapsed_ms = measure_request(
        api_client,
        "get",
        "/portfolios/P10001/holdings"
    )

    assert response.status_code == 200

    assert elapsed_ms < MAX_LATENCY_MS, (
        f"Holdings response time {elapsed_ms:.2f}ms "
        f"exceeds {MAX_LATENCY_MS}ms threshold"
    )


def test_risk_latency(api_client):
    """Risk endpoint should respond within 5 seconds."""

    response, elapsed_ms = measure_request(
        api_client,
        "get",
        "/portfolios/P10001/risk"
    )

    assert response.status_code == 200

    assert elapsed_ms < MAX_LATENCY_MS, (
        f"Risk response time {elapsed_ms:.2f}ms "
        f"exceeds {MAX_LATENCY_MS}ms threshold"
    )


def test_dashboard_latency(api_client):
    """Dashboard endpoint should respond within 5 seconds."""

    response, elapsed_ms = measure_request(
        api_client,
        "get",
        "/dashboard"
    )

    assert response.status_code == 200

    assert elapsed_ms < MAX_LATENCY_MS, (
        f"Dashboard response time {elapsed_ms:.2f}ms "
        f"exceeds {MAX_LATENCY_MS}ms threshold"
    )


def test_p95_latency(api_client):
    """
    Measure multiple API requests and verify P95 latency.

    This test intentionally performs multiple requests rather than
    relying on a single request.
    """

    endpoints = [
        "/health",
        "/portfolios/P10001",
        "/portfolios",
        "/portfolios/P10001/holdings",
        "/portfolios/P10001/risk",
        "/dashboard",
    ]

    latencies = []

    for endpoint in endpoints:
        start = time.perf_counter()

        response = api_client.get(endpoint)

        elapsed_ms = (time.perf_counter() - start) * 1000

        assert response.status_code == 200

        latencies.append(elapsed_ms)

    p95 = max(latencies)

    if len(latencies) >= 2:
        sorted_latencies = sorted(latencies)

        index = int(
            0.95 * (len(sorted_latencies) - 1)
        )

        p95 = sorted_latencies[index]

    assert p95 < MAX_LATENCY_MS, (
        f"P95 latency {p95:.2f}ms "
        f"exceeds {MAX_LATENCY_MS}ms threshold"
    )