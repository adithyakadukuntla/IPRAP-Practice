"""
TC-UI-001: UI Navigation & Portfolio List Tests
Requirements: Section 18 - UI Test Cases
"""
import pytest
from playwright.async_api import async_playwright
import asyncio

class UITestBase:
    """Base class for UI tests"""
    
    def __init__(self):
        self.base_url = "http://localhost:3000"
        self.page = None
        self.browser = None
    
    async def setup(self):
        """Setup browser and page"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch()
        self.page = await self.browser.new_page()
    
    async def teardown(self):
        """Cleanup browser"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()

class TC_UI_001_Navigation(UITestBase):
    """Navigate to portfolio list page"""
    
    async def execute(self):
        """Execute test"""
        await self.setup()
        
        try:
            # Navigate to app
            await self.page.goto(f"{self.base_url}/portfolios")
            
            # Check page loaded
            title = await self.page.title()
            assert "Portfolio" in title or "IPRAP" in title, f"Unexpected page title: {title}"
            
            # Check main elements
            await self.page.wait_for_selector("table, [data-testid='portfolio-list']", timeout=5000)
            
            print(f"✓ TC-UI-001: Portfolio list page loaded")
            return True
        except Exception as e:
            print(f"✗ TC-UI-001 FAILED: {str(e)}")
            return False
        finally:
            await self.teardown()


class TC_UI_002_PortfolioSearch(UITestBase):
    """Search for portfolio by name"""
    
    async def execute(self):
        """Execute test"""
        await self.setup()
        
        try:
            # Navigate to portfolio list
            await self.page.goto(f"{self.base_url}/portfolios")
            
            # Find search input
            search_input = await self.page.query_selector("[placeholder*='Search'], [data-testid='search-input']")
            assert search_input, "Search input not found"
            
            # Search for portfolio
            await search_input.fill("Growth Portfolio")
            await self.page.wait_for_timeout(500)
            
            # Verify results filtered
            rows = await self.page.query_selector_all("table tbody tr, [data-testid='portfolio-row']")
            assert len(rows) > 0, "No search results found"
            
            # Check search result contains "Growth"
            first_row_text = await rows[0].text_content()
            assert "Growth" in first_row_text, "Search filter didn't work"
            
            print(f"✓ TC-UI-002: Portfolio search working")
            return True
        except Exception as e:
            print(f"✗ TC-UI-002 FAILED: {str(e)}")
            return False
        finally:
            await self.teardown()


class TC_UI_003_PortfolioDetail(UITestBase):
    """Click portfolio to view details"""
    
    async def execute(self):
        """Execute test"""
        await self.setup()
        
        try:
            # Navigate to portfolio list
            await self.page.goto(f"{self.base_url}/portfolios")
            
            # Click first portfolio
            portfolio_link = await self.page.query_selector("table tbody tr a, [data-testid='portfolio-link']")
            assert portfolio_link, "Portfolio link not found"
            
            await portfolio_link.click()
            
            # Wait for detail page
            await self.page.wait_for_selector("[data-testid='portfolio-detail'], .portfolio-detail", timeout=5000)
            
            # Verify detail elements
            elements = [
                "[data-testid='portfolio-name']",
                "[data-testid='portfolio-value']",
                "[data-testid='holdings-section']"
            ]
            
            for selector in elements:
                element = await self.page.query_selector(selector)
                if element:
                    break
            assert element, "Portfolio detail elements not found"
            
            print(f"✓ TC-UI-003: Portfolio detail page loaded")
            return True
        except Exception as e:
            print(f"✗ TC-UI-003 FAILED: {str(e)}")
            return False
        finally:
            await self.teardown()


class TC_UI_004_HoldingsTable(UITestBase):
    """View holdings in detail page"""
    
    async def execute(self):
        """Execute test"""
        await self.setup()
        
        try:
            # Navigate to portfolio detail
            await self.page.goto(f"{self.base_url}/portfolios/P10001")
            
            # Wait for holdings table
            await self.page.wait_for_selector("table, [data-testid='holdings-table']", timeout=5000)
            
            # Get holdings rows
            holdings_rows = await self.page.query_selector_all("table tbody tr, [data-testid='holding-row']")
            assert len(holdings_rows) > 0, "No holdings displayed"
            
            # Check for required columns
            headers = await self.page.query_selector_all("th, [data-testid='table-header']")
            header_texts = []
            for header in headers:
                text = await header.text_content()
                header_texts.append(text.strip().lower())
            
            required = ["quantity", "price", "value"]
            found = any(any(req in h for h in header_texts) for req in required)
            assert found, f"Required columns not found. Headers: {header_texts}"
            
            print(f"✓ TC-UI-004: Holdings table displayed with {len(holdings_rows)} items")
            return True
        except Exception as e:
            print(f"✗ TC-UI-004 FAILED: {str(e)}")
            return False
        finally:
            await self.teardown()


class TC_UI_005_AllocationChart(UITestBase):
    """View allocation chart"""
    
    async def execute(self):
        """Execute test"""
        await self.setup()
        
        try:
            # Navigate to portfolio detail
            await self.page.goto(f"{self.base_url}/portfolios/P10001")
            
            # Wait for allocation chart
            chart = await self.page.query_selector("[data-testid='allocation-chart'], canvas, svg.chart")
            assert chart, "Allocation chart not found"
            
            print(f"✓ TC-UI-005: Allocation chart rendered")
            return True
        except Exception as e:
            print(f"✗ TC-UI-005 FAILED: {str(e)}")
            return False
        finally:
            await self.teardown()


class TC_UI_006_PerformanceChart(UITestBase):
    """View performance chart"""
    
    async def execute(self):
        """Execute test"""
        await self.setup()
        
        try:
            # Navigate to portfolio detail
            await self.page.goto(f"{self.base_url}/portfolios/P10001")
            
            # Scroll to performance section
            performance_section = await self.page.query_selector("[data-testid='performance-section']")
            if performance_section:
                await performance_section.scroll_into_view()
            
            # Wait for chart
            chart = await self.page.query_selector("[data-testid='performance-chart'], .chart")
            assert chart, "Performance chart not found"
            
            print(f"✓ TC-UI-006: Performance chart rendered")
            return True
        except Exception as e:
            print(f"✗ TC-UI-006 FAILED: {str(e)}")
            return False
        finally:
            await self.teardown()


class TC_UI_007_RiskIndicator(UITestBase):
    """View risk indicator on portfolio"""
    
    async def execute(self):
        """Execute test"""
        await self.setup()
        
        try:
            # Navigate to portfolio list
            await self.page.goto(f"{self.base_url}/portfolios")
            
            # Find risk indicator
            risk_badge = await self.page.query_selector("[data-testid='risk-badge'], .risk-indicator, .badge")
            assert risk_badge, "Risk indicator not found"
            
            # Get risk level
            risk_text = await risk_badge.text_content()
            assert any(level in risk_text.upper() for level in ["HIGH", "MEDIUM", "LOW"]), \
                f"Invalid risk level: {risk_text}"
            
            print(f"✓ TC-UI-007: Risk indicator displayed: {risk_text}")
            return True
        except Exception as e:
            print(f"✗ TC-UI-007 FAILED: {str(e)}")
            return False
        finally:
            await self.teardown()


class TC_UI_008_Dashboard(UITestBase):
    """View dashboard with KPIs"""
    
    async def execute(self):
        """Execute test"""
        await self.setup()
        
        try:
            # Navigate to dashboard
            await self.page.goto(f"{self.base_url}/dashboard")
            
            # Wait for KPI cards
            kpi_cards = await self.page.query_selector_all("[data-testid='kpi-card'], .kpi-card, .stat-card")
            assert len(kpi_cards) > 0, "No KPI cards found"
            
            print(f"✓ TC-UI-008: Dashboard loaded with {len(kpi_cards)} KPI cards")
            return True
        except Exception as e:
            print(f"✗ TC-UI-008 FAILED: {str(e)}")
            return False
        finally:
            await self.teardown()


# Synchronous pytest wrapper functions
@pytest.mark.asyncio
async def test_portfolio_navigation():
    """TC-UI-001: Portfolio list navigation"""
    tc = TC_UI_001_Navigation()
    result = await tc.execute()
    assert result


@pytest.mark.asyncio
async def test_portfolio_search():
    """TC-UI-002: Portfolio search"""
    tc = TC_UI_002_PortfolioSearch()
    result = await tc.execute()
    assert result


@pytest.mark.asyncio
async def test_portfolio_detail():
    """TC-UI-003: Portfolio detail page"""
    tc = TC_UI_003_PortfolioDetail()
    result = await tc.execute()
    assert result


@pytest.mark.asyncio
async def test_holdings_table():
    """TC-UI-004: Holdings table"""
    tc = TC_UI_004_HoldingsTable()
    result = await tc.execute()
    assert result


@pytest.mark.asyncio
async def test_allocation_chart():
    """TC-UI-005: Allocation chart"""
    tc = TC_UI_005_AllocationChart()
    result = await tc.execute()
    assert result


@pytest.mark.asyncio
async def test_performance_chart():
    """TC-UI-006: Performance chart"""
    tc = TC_UI_006_PerformanceChart()
    result = await tc.execute()
    assert result


@pytest.mark.asyncio
async def test_risk_indicator():
    """TC-UI-007: Risk indicator"""
    tc = TC_UI_007_RiskIndicator()
    result = await tc.execute()
    assert result


@pytest.mark.asyncio
async def test_dashboard():
    """TC-UI-008: Dashboard view"""
    tc = TC_UI_008_Dashboard()
    result = await tc.execute()
    assert result
