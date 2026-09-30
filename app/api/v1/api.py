from fastapi import APIRouter
from app.api.v1.endpoints import curate, tasks, drafts, system

api_router = APIRouter()

api_router.include_router(curate.router, tags=["Curation"])
api_router.include_router(tasks.router, tags=["Task Progress"])
api_router.include_router(drafts.router, tags=["Drafts"])
api_router.include_router(system.router, tags=["System"])

