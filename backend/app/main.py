from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware


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


app.include_router(api_router)
