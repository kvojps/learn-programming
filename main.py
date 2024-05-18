from core.infrastructure.orm.models import create_tables
from core.infrastructure.orm.models.person import Person
from core.infrastructure.settings.db import get_session

if __name__ == "__main__":
    create_tables()

    with get_session() as session:
        person = Person(name="John", age=30)
        session.add(person)
        session.commit()
        print("Person added successfully!")
