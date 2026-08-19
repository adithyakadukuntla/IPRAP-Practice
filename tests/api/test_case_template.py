"""
Test Case Template
Standardized structure for all test cases per Participant 8 PDF Section 8
"""

class TestCase:
    """Base test case structure"""
    
    def __init__(
        self,
        test_id: str,
        requirement_id: str,
        title: str,
        preconditions: list,
        test_data: dict,
        steps: list,
        expected_result: str,
        test_type: str = "Functional"
    ):
        self.test_id = test_id
        self.requirement_id = requirement_id
        self.title = title
        self.preconditions = preconditions
        self.test_data = test_data
        self.steps = steps
        self.expected_result = expected_result
        self.actual_result = None
        self.status = "Not Run"
        self.evidence = None
        self.defect_id = None
        self.retest_status = None
        self.test_type = test_type
        self.execution_time = None
        self.executed_by = None
        self.executed_date = None
    
    def execute(self):
        """Execute test case - to be overridden"""
        pass
    
    def to_dict(self):
        """Convert to dictionary for reporting"""
        return {
            "Test_ID": self.test_id,
            "Requirement_ID": self.requirement_id,
            "Title": self.title,
            "Test_Type": self.test_type,
            "Preconditions": self.preconditions,
            "Test_Data": self.test_data,
            "Steps": self.steps,
            "Expected_Result": self.expected_result,
            "Actual_Result": self.actual_result,
            "Status": self.status,
            "Evidence": self.evidence,
            "Defect_ID": self.defect_id,
            "Retest_Status": self.retest_status,
            "Execution_Time": self.execution_time,
            "Executed_By": self.executed_by,
            "Executed_Date": self.executed_date
        }


# Test ID Convention (Section 7 of PDF)
TEST_ID_PATTERNS = {
    "FUNCTIONAL": "TC-FUNC-{:03d}",
    "API": "TC-API-{:03d}",
    "UI": "TC-UI-{:03d}",
    "DATA": "TC-DATA-{:03d}",
    "E2E": "TC-E2E-{:03d}",
    "SECURITY": "TC-SEC-{:03d}",
    "PERFORMANCE": "TC-PERF-{:03d}"
}

# Test Status Values
TEST_STATUS = {
    "PASS": "PASS",
    "FAIL": "FAIL",
    "BLOCKED": "BLOCKED",
    "NOT_RUN": "Not Run",
    "IN_PROGRESS": "In Progress"
}
