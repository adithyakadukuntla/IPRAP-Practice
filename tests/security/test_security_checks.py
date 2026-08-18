import os
import re
from pathlib import Path

import requests


BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_env_file_not_committed():
    result = os.popen(
        "git ls-files"
    ).read().splitlines()

    assert ".env" not in result


def test_env_example_exists():
    assert Path(".env.example").exists()


def test_repository_has_no_obvious_hardcoded_secrets():
    patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
        r'secret[_-]?key\s*=\s*["\'][^"\']+["\']',
        r'aws[_-]?secret[_-]?access[_-]?key\s*=\s*["\'][^"\']+["\']',
    ]

    ignored = {
        ".env.example",
        ".git",
        ".pytest_cache",
        "__pycache__",
        "node_modules",
    }

    for path in Path(".").rglob("*"):
        if not path.is_file():
            continue

        if any(part in ignored for part in path.parts):
            continue

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except Exception:
            continue

        for pattern in patterns:
            assert not re.search(
                pattern,
                content,
                re.IGNORECASE
            ), f"Possible hardcoded secret in {path}"


def test_invalid_portfolio_does_not_expose_sensitive_information():
    response = requests.get(
        f"{BASE_URL}/portfolios/PXXXX"
    )

    assert response.status_code == 404

    body = response.text.lower()

    forbidden = [
        "traceback",
        "password",
        "secret_key",
        "aws_secret",
        "access_key",
    ]

    for value in forbidden:
        assert value not in body