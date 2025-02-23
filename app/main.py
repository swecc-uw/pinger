from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging
from pathlib import Path

from app.core.config import get_settings
from app.api.hosts import router as hosts_router
from app.db.base import engine, Base
from app.services.monitor import start_monitor_task

BASE_DIR = Path(__file__).resolve().parent

settings = get_settings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

app.include_router(hosts_router)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await start_monitor_task()