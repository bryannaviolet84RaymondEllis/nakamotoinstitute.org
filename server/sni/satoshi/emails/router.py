from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sni.database import get_db

from . import service
from .schemas import (
    EmailBaseModel,
    EmailDetailModel,
    EmailSource,
    EmailThreadBaseModel,
    EmailThreadModel,
    SatoshiEmailModel,
)

router = APIRouter()


@router.get("", response_model=List[EmailBaseModel])
async def get_emails(db: AsyncSession = Depends(get_db)):
    return await service.get_all_emails(db_session=db)


@router.get("/threads", response_model=List[EmailThreadBaseModel])
async def get_email_threads(db: AsyncSession = Depends(get_db)):
    return await service.get_threads(db_session=db)


@router.get("/{source}", response_model=List[SatoshiEmailModel])
async def get_emails_by_source(source: EmailSource, db: AsyncSession = Depends(get_db)):
    return await service.get_satoshi_emails_by_source(source, db_session=db)


@router.get("/{source}/threads", response_model=List[EmailThreadBaseModel])
async def get_email_threads_by_source(
    source: EmailSource, db: AsyncSession = Depends(get_db)
):
    return await service.get_threads_by_source(source, db_session=db)


@router.get(
    "/{source}/threads/{thread_id}",
    response_model=EmailThreadModel,
)
async def get_email_thread_by_source(
    source: EmailSource,
    thread_id: int,
    satoshi: bool = False,
    db: AsyncSession = Depends(get_db),
):
    thread = await service.get_thread(thread_id, db_session=db, emails=True)
    if not thread or thread.source != source:
        raise HTTPException(status_code=404, detail="Email thread not found")

    previous_thread = await service.get_thread(
        thread_id - 1, db_session=db, emails=False
    )
    next_thread = await service.get_thread(thread_id + 1, db_session=db, emails=False)

    return {
        "emails": thread.emails,
        "thread": thread,
        "previous": previous_thread,
        "next": next_thread,
    }


@router.get("/{source}/{satoshi_id}", response_model=EmailDetailModel)
async def get_email_by_source(
    source: EmailSource,
    satoshi_id: int,
    db: AsyncSession = Depends(get_db),
):
    email = await service.get_satoshi_email_by_source(source, satoshi_id, db_session=db)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    previous_email = await service.get_email(satoshi_id - 1, db_session=db)
    next_email = await service.get_email(satoshi_id + 1, db_session=db)

    return {"email": email, "previous": previous_email, "next": next_email}
