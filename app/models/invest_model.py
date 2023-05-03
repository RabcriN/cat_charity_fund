from datetime import datetime

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, Integer,
                        select)
from sqlalchemy.ext.asyncio import AsyncSession


class InvestModel:
    full_amount = Column(Integer, CheckConstraint('full_amount > 0'))
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    @classmethod
    async def get_not_fully_invested(cls, session=AsyncSession):
        not_invested = await session.execute(
            select(cls).where(
                cls.fully_invested is not True
            )
        )
        return not_invested.scalars().all()

    def mark_as_fully_invested(self):
        self.invested_amount = self.full_amount
        self.fully_invested = True
        self.close_date = datetime.now()

    def how_many_we_need_to_close(self):
        return self.full_amount - self.invested_amount
