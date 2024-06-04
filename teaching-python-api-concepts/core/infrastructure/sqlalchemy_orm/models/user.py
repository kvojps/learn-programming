from sqlalchemy import Column, Integer, String
from core.infrastructure.settings.db import SqlAlchemyBaseEntity


class User(SqlAlchemyBaseEntity):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
