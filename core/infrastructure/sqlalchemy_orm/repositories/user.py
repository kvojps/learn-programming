from core.domain.user import User
from core.infrastructure.repositories.user import IUserRepository
from core.infrastructure.sqlalchemy_orm.models.user import User as SqlAlchemyUser


class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, session):
        self.session = session

    def create_user(self, user: User) -> User:
        sql_alchemy_user = SqlAlchemyUser(
            name=user.name, email=user.email, password=user.password
        )

        self.session.add(sql_alchemy_user)
        self.session.commit()
        self.session.refresh(sql_alchemy_user)

        user.id = int(sql_alchemy_user.id)
        return user

    def get_users(self) -> list[User]:
        sql_alchemy_users = self.session.query(SqlAlchemyUser).all()

        return [
            User(
                id=int(user.id),
                name=str(user.name),
                email=str(user.email),
                password=str(user.password),
            )
            for user in sql_alchemy_users
        ]

    def get_user_by_id(self, id) -> User:
        sql_alchemy_user = (
            self.session.query(SqlAlchemyUser).filter(User.id == id).first()
        )

        return User(
            id=int(sql_alchemy_user.id),
            name=str(sql_alchemy_user.name),
            email=str(sql_alchemy_user.email),
            password=str(sql_alchemy_user.password),
        )

    def update_user(self, id, user: User) -> User:
        sql_alchemy_user_to_update = (
            self.session.query(SqlAlchemyUser).filter(User.id == id).first()
        )
        sql_alchemy_user_to_update.name = user.name
        sql_alchemy_user_to_update.email = user.email
        sql_alchemy_user_to_update.password = user.password

        self.session.commit()
        self.session.refresh(sql_alchemy_user_to_update)

        user.id = int(sql_alchemy_user_to_update.id)
        return user

    def delete_user(self, id) -> None:
        user_to_delete = (
            self.session.query(SqlAlchemyUser).filter(User.id == id).first()
        )

        self.session.delete(user_to_delete)
        self.session.commit()
