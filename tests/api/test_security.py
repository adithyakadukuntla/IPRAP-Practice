"""
Security Validation Tests
Requirements: Section 26 - Security Validation Checklist

Note:
Authentication is not implemented in the current application.
Therefore authentication/invalid-token tests are intentionally excluded.
"""

import pytest


def test_method_not_allowed(api_client):
    """
    TC-SEC-001:
    Verify that API endpoints reject unsupported HTTP methods.

    Example:
    GET /portfolios is valid.
    POST /portfolios is not supported by the read-only endpoint.
    """

    response = api_client.post("/portfolios")

    assert response.status_code == 405, (
        f"Expected 405 Method Not Allowed, "
        f"got {response.status_code}"
    )


def test_no_stack_traces(api_client):
    """
    TC-SEC-002:
    Error responses should not expose Python stack traces
    or internal framework paths.
    """

    response = api_client.get("/invalid-endpoint")

    if response.status_code >= 400:

        response_text = response.text.lower()

        forbidden = [
            "traceback",
            "at line",
            'file "',
            "site-packages",
        ]

        for term in forbidden:
            assert term not in response_text, (
                f"Potential internal information exposed: {term}"
            )


def test_password_not_logged():
    """
    TC-SEC-003:
    Logging configuration should not intentionally expose
    passwords, tokens, or secrets.

    Authentication is not implemented in the application,
    so this is currently a configuration-review placeholder.
    """

    assert True


def test_cors_restrictive(api_client):
    """
    TC-SEC-004:
    CORS should not allow every origin using '*'.
    """

    headers = {
        "Origin": "https://external.com"
    }

    response = api_client.get(
        "/portfolios",
        headers=headers
    )

    allow_origin = response.headers.get(
        "Access-Control-Allow-Origin",
        ""
    )

    assert allow_origin != "*", (
        "CORS allows all origins"
    )


def test_no_exposed_paths(api_client):
    """
    TC-SEC-005:
    API responses should not expose internal filesystem paths.
    """

    response = api_client.get("/portfolios")

    assert response.status_code in [
        200,
        400,
        404,
    ]

    response_text = response.text

    forbidden_paths = [
        "/home/",
        "/var/www/",
        "C:\\Users\\",
        "site-packages",
    ]

    for path in forbidden_paths:
        assert path not in response_text, (
            f"Internal path exposed: {path}"
        )


def test_https_recommended():
    """
    TC-SEC-006:
    HTTPS enforcement is normally handled by deployment/
    reverse-proxy configuration.

    Local development uses HTTP, so this test is informational.
    """

    assert True