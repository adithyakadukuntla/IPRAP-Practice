from fastapi import FastAPI

from routers import health
from routers import portfolios
from routers import holdings
from routers import allocation
from routers import performance
from routers import risk
from routers import clients


app = FastAPI(
    title="Investment Portfolio Risk & Analytics API",
    description="REST API for Investment Portfolio Risk & Analytics Platform",
    version="1.0.0"
)


app.include_router(health.router)
app.include_router(portfolios.router)
app.include_router(holdings.router)
app.include_router(allocation.router)
app.include_router(performance.router)
app.include_router(risk.router)
app.include_router(clients.router)


@app.get("/")
def root():
    return {
        "service": "ipra-api",
        "version": "1.0.0",
        "docs": "/docs"
    }