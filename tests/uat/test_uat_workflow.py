def test_uat_complete_portfolio_workflow(api_client):
    # 1. User opens dashboard
    dashboard = api_client.get("/dashboard")

    assert dashboard.status_code == 200

    # 2. User opens portfolio
    portfolio = api_client.get(
        "/portfolios/P10001"
    )

    assert portfolio.status_code == 200

    # 3. User views holdings
    holdings = api_client.get(
        "/portfolios/P10001/holdings"
    )

    assert holdings.status_code == 200

    # 4. User views performance
    performance = api_client.get(
        "/portfolios/P10001/performance"
    )

    assert performance.status_code == 200

    # 5. User views risk
    risk = api_client.get(
        "/portfolios/P10001/risk"
    )

    assert risk.status_code == 200

    # 6. User views allocation
    allocation = api_client.get(
        "/portfolios/P10001/allocation"
    )

    assert allocation.status_code == 200