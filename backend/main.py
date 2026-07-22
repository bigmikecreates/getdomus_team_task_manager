from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1.auth import router as auth_router
from backend.api.v1.dashboard import router as dashboard_router
from backend.api.v1.developers import router as developers_router
from backend.api.v1.tasks import router as tasks_router
from backend.api.v1.presence import router as presence_router
from backend.core.config import settings

app = FastAPI(
    title="GetDomus Team Task Manager",
    description="Task management app for distributed engineering teams",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(developers_router)
app.include_router(dashboard_router)
app.include_router(presence_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
