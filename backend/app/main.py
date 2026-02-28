from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.datasets import router as datasets_router

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
api_router = APIRouter(prefix="/api")


@api_router.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


api_router.include_router(auth_router)
api_router.include_router(datasets_router)

app.include_router(api_router)
