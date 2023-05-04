from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = (
        await charity_project_crud.get_charity_project_id_by_name(
            charity_project_name,
            session)
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Благотворительный проект не найден!'
        )
    return charity_project


async def check_charity_project_invested_amount(
        project_id: int,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_charity_project_is_not_closed(
        project_id: int,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_full_amount_not_less_than_before(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(project_id, session)
    if obj_in.full_amount and obj_in.full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя устанавливать требуемую сумму меньше уже внесённой!'
        )


async def check_charity_project_before_edit(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
):
    await check_charity_project_is_not_closed(project_id, session)
    await check_full_amount_not_less_than_before(project_id, obj_in, session)
