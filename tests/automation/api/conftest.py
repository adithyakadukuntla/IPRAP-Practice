import pytest
import json
import os
from pathlib import Path
import requests
from typing import Dict, Any

# Load test data
TEST_DATA_PATH = Path(__file__).parent.parent.parent / "test-cases" / "test_data.json"

@pytest.fixture(scope="session")
def test_data():
    """Load test data from JSON file"""
    with open(TEST_DATA_PATH, 'r') as f:
        return json.load(f)

@pytest.fixture
def api_client():
    """Create API client"""
    class APIClient:
        def __init__(self, base_url="http://localhost:8000/api/v1"):
            self.base_url = base_url
            self.session = requests.Session()
        
        def get(self, endpoint, params=None, headers=None):
            return self.session.get(f"{self.base_url}{endpoint}", params=params, headers=headers)
        
        def post(self, endpoint, data=None, json=None, headers=None):
            return self.session.post(f"{self.base_url}{endpoint}", data=data, json=json, headers=headers)
        
        def close(self):
            self.session.close()
    
    return APIClient()

@pytest.fixture
def auth_headers():
    """Return auth headers for API requests"""
    return {"Authorization": "Bearer test-token", "Content-Type": "application/json"}

@pytest.fixture
def portfolio_data(test_data):
    """Get portfolio test data"""
    return test_data.get("portfolios", [])

@pytest.fixture
def holding_data(test_data):
    """Get holding test data"""
    return test_data.get("holdings", [])

@pytest.fixture
def client_data(test_data):
    """Get client test data"""
    return test_data.get("clients", [])

@pytest.fixture
def performance_data(test_data):
    """Get performance test data"""
    return test_data.get("performance", [])

@pytest.fixture
def risk_data(test_data):
    """Get risk test data"""
    return test_data.get("risk_metrics", [])

@pytest.fixture
def test_case_template():
    """Test case template"""
    return {
        "test_id": "",
        "requirement_id": "",
        "title": "",
        "preconditions": [],
        "test_data": {},
        "steps": [],
        "expected_result": "",
        "actual_result": "",
        "status": "Not Run",
        "evidence": "",
        "defect_id": None,
        "retest_status": None
    }
