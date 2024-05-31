# 2 - Gerenciamento de erros na camada de repositório
O código desta aula está disponível na branch indicada abaixo:
- [(Branch: feat/lesson-3-repo-error-handling)](https://github.com/kvojps/learn-programming/tree/feat/lesson-3-error-handling)

## 2.1 Implementação

``` python
@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    except IntegrityError as e:
        session.rollback()
        raise e
    except IndexError as e:
        session.rollback()
        raise e
    finally:
        session.close()
```

Como explicado na aula sobre o "repository pattern", a função `get_session` gerencia o ciclo de vida da sessão com o banco de dados. Isso inclui garantir que a sessão seja aberta, usada e fechada corretamente. Além disso, ela agora lida com erros que podem ocorrer durante o uso da sessão. Em casos de erro, como um `IntegrityError`, por exemplo, ocorre um rollback. Isso é fundamental para garantir a integridade dos dados e evitar que operações parciais sejam confirmadas no banco de dados em situações inesperadas.

``` python
# Definição da tabela usuário
class User(SqlAlchemyBaseEntity):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# Método do repositório para atualizar um usuário
def update_user(self, id, user: User) -> User:
    with get_session() as session:
        sql_alchemy_user_to_update = self._get_user_by_id(session, id)

        sql_alchemy_user_to_update.name = user.name
        sql_alchemy_user_to_update.email = user.email
        sql_alchemy_user_to_update.password = user.password

        session.commit()
        session.refresh(sql_alchemy_user_to_update)

        user.id = int(sql_alchemy_user_to_update.id)

        return user
```

``` python
    def _get_user_by_id(self, session, id_user: int) -> SqlAlchemyUser:
        if (
            sql_alchemy_user := (
                session.query(SqlAlchemyUser)
                .filter(SqlAlchemyUser.id == id_user)
                .first()
            )
        ) is None:
            raise IndexError("User not found")

        return sql_alchemy_user

```

Na entidade User, o campo email é configurado como único. Isso significa que ao tentar cadastrar mais de um usuário com o mesmo email, o erro é devidamente gerenciado pela função get_session. Nesse caso, a função detecta a tentativa de duplicação de emails, e em resposta, retorna um Integrity Error com a informação sobre os campos inválidos. O IndexError ocorre apenas quando se tenta obter um usuário pelo ID e este não existe no sistema.

Por fim, abaixo segue o código completo referente a implementação repositório do usuário:

``` python
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
            sql_alchemy_user = self._get_user_by_id(session, id)

            return User(
                id=int(sql_alchemy_user.id),
                name=str(sql_alchemy_user.name),
                email=str(sql_alchemy_user.email),
                password=str(sql_alchemy_user.password),
            )

    def update_user(self, id, user: User) -> User:
        with get_session() as session:
            sql_alchemy_user_to_update = self._get_user_by_id(session, id)

            sql_alchemy_user_to_update.name = user.name
            sql_alchemy_user_to_update.email = user.email
            sql_alchemy_user_to_update.password = user.password

            session.commit()
            session.refresh(sql_alchemy_user_to_update)

            user.id = int(sql_alchemy_user_to_update.id)

            return user

    def delete_user(self, id) -> None:
        with get_session() as session:
            sql_alchemy_user = self._get_user_by_id(session, id)

            session.delete(sql_alchemy_user)
            session.commit()

    def _get_user_by_id(self, session, id_user: int) -> SqlAlchemyUser:
        if (
            sql_alchemy_user := (
                session.query(SqlAlchemyUser)
                .filter(SqlAlchemyUser.id == id_user)
                .first()
            )
        ) is None:
            raise IndexError("User not found")

        return sql_alchemy_user
```

Observe que a função _get_user_by_id, encarregada de retornar um usuário ou lançar um IndexError caso ele não exista, é reutilizada nos métodos de obter, atualizar e excluir usuários por ID.

É ideal que os erros sejam tratados em várias camadas do sistema, desde as mais internas até chegarem ao usuário final de maneira amigável. Esse tratamento amigável dos erros ocorrerá especificamente na camada da API, onde as mensagens de erro serão formatadas de forma clara e compreensível para o usuário, facilitando a identificação e resolução de problemas durante a interação com o sistema.

## 2.2. Execução do código
- Acesse a branch **feat/lesson-3-repo-error-handling** para verificar o código desta aula.
- Execute o arquivo **main.py** na raíz do projeto;
  - Este arquivo executa operações no banco de dados por meio dos artefatos construídos nessa aula;