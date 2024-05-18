from core.infrastructure.settings.db import engine
from .person import Person


def create_tables():
    Person.metadata.create_all(engine)
