from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.invest_model import InvestModel


class CharityProject(Base, InvestModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
