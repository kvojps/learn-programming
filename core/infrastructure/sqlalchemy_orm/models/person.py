from sqlalchemy import Column, Integer, String
from core.infrastructure.settings.db import SqlAlchemyBaseEntity


class Person(SqlAlchemyBaseEntity):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
