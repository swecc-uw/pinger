
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.schemas.host import HostCreate, HostResponse
from app.models.host import Host

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@router.get("/hosts", response_model=List[HostResponse])
async def read_hosts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Host))
    hosts = result.scalars().all()
    return hosts

@router.post("/hosts", response_model=HostResponse)
async def create_host(
    email: str = Form(...),
    host: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    host_data = HostCreate(email=email, host=host)
    db_host = Host(**host_data.dict())
    db.add(db_host)
    await db.commit()
    await db.refresh(db_host)
    return db_host