from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt, root_validator


class CharityProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    @root_validator(
        skip_on_failure=True
    )
    def check_name_and_description(cls, values):
        if values['name'] == '':
            raise ValueError(
                'Имя не должно быть пустым'
            )
        if values['name'] and len(values['name']) > 100:
            raise ValueError(
                'Имя не может быть больше 100 символов'
            )
        if values['description'] == '':
            raise ValueError(
                'Описание не должно быть пустым'
            )
        return values


class CharityProjectCreate(CharityProjectUpdate):
    name: str
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
