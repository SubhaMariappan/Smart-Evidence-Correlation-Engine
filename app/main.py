import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.router import api_router
from app.web.router import web_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered Digital Forensics and Evidence Correlation Platform",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for safe cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists & mount static files
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Register API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Register Web Dashboard Router
app.include_router(web_router)

@app.get("/", include_in_schema=False)
def root():
    """Redirect root path to the forensic workstation login page."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/login")


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint to verify backend status."""
    return {
        "status": "healthy",
        "service": "SECE-Backend",
        "version": settings.VERSION
    }
