from core.domain.user import User
from core.infrastructure.repositories.user import IUserRepository
from core.infrastructure.settings.db import get_session
from core.infrastructure.sqlalchemy_orm.models.user import User as SqlAlchemyUser


class SqlAlchemyUserRepository(IUserRepository):
    def create_user(self, user: User) -> User:
        with get_session() as session:
            sql_alchemy_user = SqlAlchemyUser(
                name=user.name, email=user.email, password=user.password
            )

            session.add(sql_alchemy_user)
            session.commit()
            session.refresh(sql_alchemy_user)

            user.id = int(sql_alchemy_user.id)

            return user

    def get_users(self) -> list[User]:
        with get_session() as session:
            sql_alchemy_users = session.query(SqlAlchemyUser).all()

            return [
                User(
                    id=int(sql_alchemy_user.id),
                    name=str(sql_alchemy_user.name),
                    email=str(sql_alchemy_user.email),
                    password=str(sql_alchemy_user.password),
                )
                for sql_alchemy_user in sql_alchemy_users
            ]

    def get_user_by_id(self, id) -> User:
        with get_session() as session:
            sql_alchemy_user = (
                session.query(SqlAlchemyUser).filter(SqlAlchemyUser.id == id).first()
            )

            return User(
                id=int(sql_alchemy_user.id),
                name=str(sql_alchemy_user.name),
                email=str(sql_alchemy_user.email),
                password=str(sql_alchemy_user.password),
            )

    def update_user(self, id, user: User) -> User:
        with get_session() as session:
            sql_alchemy_user_to_update = (
                session.query(SqlAlchemyUser).filter(SqlAlchemyUser.id == id).first()
            )
            sql_alchemy_user_to_update.name = user.name
            sql_alchemy_user_to_update.email = user.email
            sql_alchemy_user_to_update.password = user.password

            session.commit()
            session.refresh(sql_alchemy_user_to_update)

            user.id = int(sql_alchemy_user_to_update.id)

            return user

    def delete_user(self, id) -> None:
        with get_session() as session:
            user_to_delete = (
                session.query(SqlAlchemyUser).filter(SqlAlchemyUser.id == id).first()
            )

            session.delete(user_to_delete)
            session.commit()
