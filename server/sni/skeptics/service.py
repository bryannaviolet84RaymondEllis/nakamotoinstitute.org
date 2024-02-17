from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sni.models import Skeptic


async def get_all(*, db_session: AsyncSession) -> List[Skeptic]:
    query = select(Skeptic).order_by(Skeptic.date)

    result = await db_session.scalars(query)
    return result.all()
