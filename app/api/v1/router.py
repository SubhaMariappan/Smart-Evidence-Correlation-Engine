from fastapi import APIRouter
from app.api.v1.endpoints import auth, cases, evidence, entities, correlation, summary

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(cases.router, prefix="/cases", tags=["Case Management"])
api_router.include_router(evidence.router, tags=["Evidence Management"])
api_router.include_router(entities.router, tags=["Entity Extraction & Resolution"])
api_router.include_router(correlation.router, tags=["Evidence Correlation & Link Discovery"])
api_router.include_router(summary.router, tags=["Investigation Summary"])
