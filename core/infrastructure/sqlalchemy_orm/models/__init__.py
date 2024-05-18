from core.infrastructure.settings.db import engine
from .user import User


def create_tables():
    User.metadata.create_all(engine)
