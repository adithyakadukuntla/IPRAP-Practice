from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

from routers import health
from routers import portfolios
from routers import holdings
from routers import allocation
from routers import performance
from routers import risk
from routers import clients
from routers import dashboard


app = FastAPI(
    title="Investment Portfolio Risk & Analytics API",
    description="REST API for Investment Portfolio Risk & Analytics Platform",
    version="1.0.0"
)

# Configure CORS for local frontend development (always enabled for common localhost origins)
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


app.include_router(health.router)
app.include_router(portfolios.router)
app.include_router(holdings.router)
app.include_router(allocation.router)
app.include_router(performance.router)
app.include_router(risk.router)
app.include_router(clients.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "service": "ipra-api",
        "version": "1.0.0",
        "docs": "/docs"
    }