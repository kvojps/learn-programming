from core.infrastructure.settings.db import get_session
from core.infrastructure.sqlalchemy_orm.models import create_tables
from core.infrastructure.sqlalchemy_orm.models.user import User

if __name__ == "__main__":
    create_tables()

    with get_session() as session:
        user = User(name="John Doe", email="johndoe@gmail.com", password="password")
        session.add(user)
        session.commit()
        print("User added successfully!")
