from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_edit,
                                check_charity_project_exists,
                                check_charity_project_invested_amount,
                                check_charity_project_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.invest_process import make_transaction

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. \n
    Создаёт благотворительный проект."""
    await check_charity_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session,
    )
    await make_transaction(session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. \n
    Удаляет проект. Нельзя удалить проект, в который уже были
     инвестированы средства, его можно только закрыть."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_invested_amount(
        project_id,
        session
    )
    charity_project = await charity_project_crud.remove(
        charity_project,
        session
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. \n
    Закрытый проект нельзя редактировать; нельзя установить требуемую
     сумму меньше уже вложенной."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await check_charity_project_name_duplicate(obj_in.name, session)

    await check_charity_project_before_edit(project_id, obj_in, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
