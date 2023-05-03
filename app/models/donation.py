from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.invest_model import InvestModel


class Donation(Base, InvestModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
