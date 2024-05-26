# 2 - Repository pattern [(Branch: feat/lesson-2-repo-pattern)](https://github.com/kvojps/learn-programming/tree/feat/lesson-2-repo-pattern)

## 2.1 O que é o Repository pattern?
O Repository Pattern cria uma camada de abstração entre a aplicação e a fonte de dados. Ele encapsula a lógica necessária para acessar, armazenar e gerenciar dados, proporcionando uma interface que permite a comunicação com a fonte de dados sem que a lógica de negócios precise conhecer os detalhes da implementação da persistência.

## 2.2 Implementação do Repository pattern no projeto

### 2.2.1 Criação do módulo domain
A módulo de domínio representa as entidades que refletem a modelagem do sistema. Esta módulo deve ignorar totalmente os detalhes de persistência de dados. Essas tarefas de persistência devem ser executadas pela módulo de infraestrutura, por isso na módulo de infraestrutura estão definidos os modelos que serão usados para persistência de dados.

- Para modelar as entidades de domínio vamos utilizar a biblioteca Pydantic, para isso execute o comando para atualizar suas dependências:
```bash
pip install -r requirements.txt
```
- Foi criada a entidade User no módulo de domínio, onde a respectiva modelagem no módulo do ORM é atendida;
  - Para isso, houve uma alteração na entidade person para user no módulo infrastructure/sqlalchemy_orm/models/;

### 2.2.2 Criação do módulo repositories
#### 2.2.2.1 Interfaces
- Foi criado um módulo repositories na raíz do módulo infrastructure, onde vão ficar as interfaces de repositórios.
  - Por que usar interfaces? Os métodos de operação no banco de dados serão sempre os mesmos, o que pode variar é a implementação conforme o ORM utilizado. Utilizar interfaces garante que nossas definições de código permaneçam agnósticas em relação à implementação real. Além disso, facilita os testes, permitindo que as interfaces sejam implementadas de forma específica para testes.

  ``` python
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

  ```
  - A partir do uso da interface acima, é possível implementá-la para testes e diferentes ORMs. Isso garante que possamos usar essa abstração em diversas partes do código, mantendo-o agnóstico em relação à implementação específica.

#### 2.2.2.1 Implementações
- Este é um exemplo de implementação da interface do repositório de usuário para o contexto do SQLAlchemy:

``` python
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
            self.session.query(SqlAlchemyUser).filter(SqlAlchemyUser.id == id).first()
        )

        return User(
            id=int(sql_alchemy_user.id),
            name=str(sql_alchemy_user.name),
            email=str(sql_alchemy_user.email),
            password=str(sql_alchemy_user.password),
        )

    def update_user(self, id, user: User) -> User:
        sql_alchemy_user_to_update = (
            self.session.query(SqlAlchemyUser).filter(SqlAlchemyUser.id == id).first()
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
            self.session.query(SqlAlchemyUser).filter(SqlAlchemyUser.id == id).first()
        )

        self.session.delete(user_to_delete)
        self.session.commit()
```

### 2.2.3 Execução do código
- Acesse a branch **feat/lesson-2-repo-pattern** para verificar o código desta aula.
- Execute o arquivo **main.py** na raíz do projeto;
  - Este arquivo executa operações no banco de dados por meio dos artefados construídos nessa aula;
