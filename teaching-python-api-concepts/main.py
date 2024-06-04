from core.domain.user import User
from core.infrastructure.sqlalchemy_orm.models import create_tables
from core.infrastructure.sqlalchemy_orm.repositories.user import (
    SqlAlchemyUserRepository,
)

if __name__ == "__main__":
    create_tables()

    user_repository = SqlAlchemyUserRepository()

    user = User(id=None, name="John Doe", email="teste@gmail.com", password="123456")

    # Create user
    user_create_response = user_repository.create_user(user)
    print("--- Create user ---")
    print(user_create_response)
    print("--- *** ---")

    # Get all users
    users_get_all_response = user_repository.get_users()
    print("--- Get all users ---")
    print(users_get_all_response)
    print("--- *** ---")

    # Update user
    user_update_response = user_repository.update_user(
        user_create_response.id,
        User(id=None, name="John Doe Updated", email="asdasd", password="asdasdas"),
    )
    print("--- Update user ---")
    print(user_update_response)
    print("--- *** ---")

    # Get user by id
    user_get_by_id_response = user_repository.get_user_by_id(user_create_response.id)
    print("--- Get user by id ---")
    print(user_get_by_id_response)
    print("--- *** ---")

    # Delete user
    user_repository.delete_user(user_create_response.id)
    print("--- Delete user ---")
    print("User deleted successfully")
    print("--- *** ---")
