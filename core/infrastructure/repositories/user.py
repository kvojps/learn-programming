from abc import ABC, abstractmethod
from core.domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User: ...

    @abstractmethod
    def get_users(self) -> list[User]: ...

    @abstractmethod
    def get_user_by_id(self, id: int) -> User: ...

    @abstractmethod
    def update_user(self, id: int, user: User) -> User: ...

    @abstractmethod
    def delete_user(self, id: int) -> None: ...
