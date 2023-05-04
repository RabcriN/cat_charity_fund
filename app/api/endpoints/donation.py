from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donations import donation_crud
from app.models import User
from app.schemas.donation import (DonationBase, DonationFullResponse,
                                  DonationShortResponse)
from app.services.invest_process import make_transaction

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationFullResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. \n
    Возвращает список всех пожертвований."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationShortResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    my_donations = await donation_crud.get_my_donation(user, session)
    return my_donations


@router.post(
    '/',
    response_model=DonationShortResponse,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    await make_transaction(session)
    await session.refresh(new_donation)
    return new_donation
