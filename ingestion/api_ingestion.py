import requests


def fetch_security_data(api_url: str):
    """
    Fetch security data from REST API.
    """

    try:
        response = requests.get(
            api_url,
            timeout=30
        )

        # Raise exception for HTTP errors
        response.raise_for_status()

        data = response.json()

        return data

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Security API request timed out."
        )

    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"Security API returned HTTP error: {e}"
        )

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Security API request failed: {e}"
        )

    except ValueError as e:
        raise RuntimeError(
            f"Security API returned invalid JSON: {e}"
        )


import json
from pathlib import Path


def read_security_json(file_path: str):
    """
    Read security data from a local JSON file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Security JSON file not found: {path}"
        )

    if path.stat().st_size == 0:
        raise ValueError(
            f"Security JSON file is empty: {path}"
        )

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Invalid JSON format in {path}: {e}"
        ) from e