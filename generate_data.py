import os, json, random, math
from datetime import date, timedelta
import pandas as pd

# Deterministic generation: IDs are created first, then relationships reference those IDs.
random.seed(42)

base = r"C:\Users\Administrator\Desktop\IPRAP-Practice"
raw_dirs = [
    "data/raw/clients",
    "data/raw/portfolios",
    "data/raw/securities",
    "data/raw/holdings",
    "data/raw/portfolio_performance",
]
for d in raw_dirs:
    os.makedirs(os.path.join(base, d), exist_ok=True)

# -------------------------
# 1. CLIENTS: 50
# -------------------------
first_names = ["John","Emily","Michael","Sophia","Daniel","Olivia","James","Ava","William","Isabella",
               "Robert","Mia","David","Charlotte","Thomas","Amelia","Christopher","Harper","Matthew","Evelyn"]
last_names = ["Carter","Watson","Brown","Miller","Wilson","Taylor","Anderson","Thomas","Jackson","White",
              "Harris","Martin","Thompson","Garcia","Martinez","Robinson","Clark","Lewis","Lee","Walker"]

countries = ["USA","UK","INDIA","CANADA","GERMANY","SINGAPORE"]
clients = []
client_ids = [f"C{10001+i}" for i in range(50)]

for i, cid in enumerate(client_ids):
    clients.append({
        "client_id": cid,
        "client_name": f"{first_names[i % len(first_names)]} {last_names[i % len(last_names)]}",
        "client_type": "INDIVIDUAL" if i < 42 else "INSTITUTIONAL",
        "country": countries[i % len(countries)],
        "risk_profile": ["LOW","MEDIUM","HIGH"][i % 3],
        "created_date": (date(2025,1,15) + timedelta(days=i*7)).isoformat(),
        "status": "ACTIVE" if i < 47 else "INACTIVE"
    })

clients_df = pd.DataFrame(clients)

# -------------------------
# 2. PORTFOLIOS: 100
# -------------------------
portfolio_types = [
    ("EQUITY_GROWTH","HIGH"),
    ("INCOME","LOW"),
    ("BALANCED","MEDIUM"),
    ("INDEX","MEDIUM"),
    ("FIXED_INCOME","LOW"),
]
currencies = ["USD","GBP","EUR","INR","CAD","SGD"]

portfolios = []
portfolio_ids = [f"P{10001+i}" for i in range(100)]

for i, pid in enumerate(portfolio_ids):
    client_id = client_ids[(i * 7) % len(client_ids)]
    ptype, risk = portfolio_types[i % len(portfolio_types)]
    initial = round(random.uniform(100000, 2500000), 2)
    growth = random.uniform(-0.04, 0.18)
    current = round(initial * (1 + growth), 2)
    inception = date(2025,1,20) + timedelta(days=(i*5) % 250)
    
    portfolios.append({
        "portfolio_id": pid,
        "client_id": client_id,
        "portfolio_name": f"{ptype.replace('_',' ').title()} Portfolio",
        "portfolio_type": ptype,
        "base_currency": currencies[i % len(currencies)],
        "risk_profile": risk,
        "initial_value": initial,
        "current_value": current,
        "inception_date": inception.isoformat(),
        "status": "ACTIVE" if i < 94 else "INACTIVE"
    })

portfolios_df = pd.DataFrame(portfolios)

# -------------------------
# 3. SECURITIES: 120 JSON
# -------------------------
security_names = [
    ("Apple Inc.","AAPL","EQUITY","TECHNOLOGY","USA","USD"),
    ("Microsoft Corp.","MSFT","EQUITY","TECHNOLOGY","USA","USD"),
    ("Amazon.com Inc.","AMZN","EQUITY","CONSUMER_DISCRETIONARY","USA","USD"),
    ("Alphabet Inc.","GOOGL","EQUITY","COMMUNICATION_SERVICES","USA","USD"),
    ("NVIDIA Corp.","NVDA","EQUITY","TECHNOLOGY","USA","USD"),
    ("Tesla Inc.","TSLA","EQUITY","CONSUMER_DISCRETIONARY","USA","USD"),
    ("JPMorgan Chase & Co.","JPM","EQUITY","FINANCIALS","USA","USD"),
    ("Johnson & Johnson","JNJ","EQUITY","HEALTHCARE","USA","USD"),
    ("Visa Inc.","V","EQUITY","FINANCIALS","USA","USD"),
    ("Procter & Gamble Co.","PG","EQUITY","CONSUMER_STAPLES","USA","USD"),
    ("iShares Core S&P 500 ETF","IVV","ETF","INDEX","USA","USD"),
    ("Vanguard Total Stock Market ETF","VTI","ETF","INDEX","USA","USD"),
    ("Vanguard FTSE Europe ETF","VGK","ETF","INDEX","USA","USD"),
    ("iShares MSCI Emerging Markets ETF","EEM","ETF","INDEX","USA","USD"),
    ("Invesco QQQ","QQQ","ETF","TECHNOLOGY","USA","USD"),
    ("Apple Corporate Bond","ACB25","BOND","CORPORATE_BONDS","USA","USD"),
    ("Global Government Bond","GGB25","BOND","GOVERNMENT","UK","GBP"),
    ("India Government Bond","IGB25","BOND","GOVERNMENT","INDIA","INR"),
    ("European Investment Bond","EIB25","BOND","GOVERNMENT","GERMANY","EUR"),
    ("Singapore Treasury Bond","STB25","BOND","GOVERNMENT","SINGAPORE","SGD"),
]
securities = []
security_ids = [f"SEC{10001+i}" for i in range(120)]

for i, sid in enumerate(security_ids):
    template = security_names[i % len(security_names)]
    name, ticker, stype, sector, country, currency = template
    suffix = "" if i < len(security_names) else f" Series {i // len(security_names)+1}"
    price_base = 20 + (i * 17.37) % 480
    price = round(max(5, price_base + random.uniform(-8,8)), 2)
    ticker_final = ticker if i < len(security_names) else f"{ticker}{i//len(security_names)+1}"
    
    securities.append({
        "security_id": sid,
        "ticker_symbol": ticker_final,
        "security_name": name + suffix,
        "security_type": stype,
        "sector": sector,
        "country": country,
        "currency": currency,
        "current_price": price,
        "status": "ACTIVE"
    })

# -------------------------
# 4. HOLDINGS: 600
# Relationships are selected ONLY from existing portfolio/security IDs.
# -------------------------
holdings = []
holding_ids = [f"H{100001+i}" for i in range(600)]

for i, hid in enumerate(holding_ids):
    pid = portfolio_ids[i % len(portfolio_ids)]
    sid = security_ids[(i * 11 + i // 17) % len(security_ids)]
    sec = securities[int(sid[3:]) - 10001]
    
    quantity = round(random.uniform(10, 5000), 4)
    current_price = sec["current_price"]
    purchase_factor = random.uniform(0.78, 1.08)
    purchase_price = round(current_price * purchase_factor, 2)
    market_value = round(quantity * current_price, 2)
    as_of = date(2026,8,1) + timedelta(days=i % 10)
    
    holdings.append({
        "holding_id": hid,
        "portfolio_id": pid,
        "security_id": sid,
        "quantity": quantity,
        "purchase_price": purchase_price,
        "current_price": current_price,
        "market_value": market_value,
        "as_of_date": as_of.isoformat()
    })

holdings_df = pd.DataFrame(holdings)

# -------------------------
# 5. PERFORMANCE: 1,200
# 12 records per portfolio, with mathematically consistent returns.
# -------------------------
performance = []
performance_ids = [f"PERF{100001+i}" for i in range(1200)]

for p_idx, pid in enumerate(portfolio_ids):
    portfolio = portfolios[p_idx]
    value = portfolio["initial_value"]
    
    for month in range(12):
        idx = p_idx * 12 + month
        beginning = round(value, 2)
        monthly_return = random.uniform(-0.035, 0.055)
        ending = round(beginning * (1 + monthly_return), 2)
        return_amount = round(ending - beginning, 2)
        return_percent = round((return_amount / beginning) * 100, 4) if beginning else 0.0
        
        performance.append({
            "performance_id": performance_ids[idx],
            "portfolio_id": pid,
            "as_of_date": (date(2025,9,30) + timedelta(days=30*month)).isoformat(),
            "beginning_value": beginning,
            "ending_value": ending,
            "return_amount": return_amount,
            "return_percent": return_percent
        })
        value = ending

performance_df = pd.DataFrame(performance)

# -------------------------
# Write files
# -------------------------
clients_path = os.path.join(base, "data/raw/clients/clients.csv")
portfolios_path = os.path.join(base, "data/raw/portfolios/portfolios.csv")
securities_path = os.path.join(base, "data/raw/securities/securities.json")
holdings_path = os.path.join(base, "data/raw/holdings/holdings.csv")
performance_path = os.path.join(base, "data/raw/portfolio_performance/portfolio_performance.csv")

clients_df.to_csv(clients_path, index=False)
portfolios_df.to_csv(portfolios_path, index=False)
holdings_df.to_csv(holdings_path, index=False)
performance_df.to_csv(performance_path, index=False)

with open(securities_path, "w", encoding="utf-8") as f:
    json.dump(securities, f, indent=2)

# -------------------------
# Relationship verification
# -------------------------
assert len(clients_df) == 50
assert len(portfolios_df) == 100
assert len(securities) == 120
assert len(holdings_df) == 600
assert len(performance_df) == 1200

assert set(portfolios_df["client_id"]).issubset(set(clients_df["client_id"]))
assert set(holdings_df["portfolio_id"]).issubset(set(portfolios_df["portfolio_id"]))
assert set(holdings_df["security_id"]).issubset(set(security_ids))
assert set(performance_df["portfolio_id"]).issubset(set(portfolios_df["portfolio_id"]))

# Financial consistency checks
assert (abs(holdings_df["market_value"] - holdings_df["quantity"] * holdings_df["current_price"]) < 0.01).all()
assert (abs(performance_df["return_amount"] - (performance_df["ending_value"] - performance_df["beginning_value"])) < 0.01).all()

summary = pd.DataFrame({
    "Dataset": ["clients.csv","portfolios.csv","securities.json","holdings.csv","portfolio_performance.csv"],
    "Records": [len(clients_df),len(portfolios_df),len(securities),len(holdings_df),len(performance_df)],
    "Status": ["VALID","VALID","VALID","VALID","VALID"]
})

print(f"Created dataset package at: {base}")
print(summary.to_string(index=False))
print("\nAll foreign-key relationships and financial calculations verified successfully.")
