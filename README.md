# Sumário
- [Aula 1: ORM (Branch: feat/lesson-1-orm)](#aula-1-orm-branch-featlesson-1-orm)
- [Aula 2: Repository pattern (Branch: feat/lesson-2-repo-pattern)](#aula-2-repository-pattern-branch-featlesson-2-repo-pattern)

# Aula 1: ORM (Branch: feat/lesson-1-orm)

## 1.1 O que é um ORM?
Um ORM (Object-Relational Mapping) é uma técnica de programação que mapeia objetos definidos em uma linguagem de programação orientada a objetos para estruturas de dados em um banco de dados relacional. Isso permite que os desenvolvedores usem objetos e métodos orientados a objetos para interagir com o banco de dados, em vez de escrever consultas SQL diretamente.

## 1.2 O que é o SQLAlchemy?
O SQLAlchemy é uma biblioteca de mapeamento objeto-relacional (ORM) para Python. Ele fornece uma maneira de mapear objetos Python para tabelas em um banco de dados relacional, facilitando o desenvolvimento de aplicativos que lidam com dados de maneira orientada a objetos. SQLAlchemy suporta uma variedade de bancos de dados SQL e oferece uma API flexível e poderosa para criar consultas, gerenciar transações e interagir com o banco de dados de forma programática.

## 1.3 O que é necessário para executar o código da primeira aula?
- Acesse a branch **feat/lesson-1-orm** para verificar o código desta aula.

### 1.3.1 Criação do ambiente virtual
- Qual importância de um ambiente virtual python?
    - Isolar as dependências do seu projeto do sistema global. Isso é essencial para evitar conflitos entre diferentes projetos que possam exigir versões distintas das mesmas bibliotecas.
```bash
# Criação do ambiente virtual
python -m venv .venv

# Ativação do ambiente virtual (Windows)
.venv\Scripts\activate

# Ativação do ambiente virtual (MacOS/Linux)
.source venv/bin/activate
```

### 1.3.2 Instalação das dependências do projeto
``` bash
# Instalar dependências de dev
# Estas dependências não impactam no funcionamento do projeto
pip install -r requirements-dev.txt

# O pip-compile está disponível a partir da instalação das dependências de dev
# Um arquivo requirements.txt é gerado com as dependências versionadas
pip-compile requirements.in

# Instalar dependências do projeto
pip install -r requirements.txt
```

### 1.3.3 Criação do arquivo de variável de ambiente
Crie um arquivo .env na raíz do projeto e preencha de acordo com o .env.example.

### 1.3.4 Execução do código
- Execute o arquivo **main.py** na raíz do projeto;
  - Este arquivo executa uma inserção de dados no banco de dados por meio dos artefados construídos nessa aula;

## 1.4 Entendimento do código
### 1.4.1 Módulo core/infrastructure/settings
- O módulo settings é responsável pelas configurações necessárias para acessar recursos externos;
- O arquivo **env_handler.py** é responsável pela obtenção de váriaveis de ambiente presentes no arquivo .env;
- O arquivo **db.py** é responsável por:
    - Realizar a conexão com o banco de dados;
    - Criar uma sessão com o banco de dados;
    - Definir a classe Base do ORM SQLAlchemy que serão utilizadas por todas as classes que serão persistidas no banco de dados;

 #### 1.4.1.1 Obter sessão com o banco de dados
 ```python
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
```
A razão para usar yield em vez de return nesta função é para aproveitar a funcionalidade dos geradores e dos gerenciadores de contexto em Python.

Se você usasse return em vez de yield, a função retornaria a sessão, mas não teria controle sobre o que acontece com ela depois. Você não teria garantia de que a sessão seria fechada corretamente, o que poderia levar a vazamentos de recursos.

Ao usar yield, você transforma a função get_session em um gerador. Isso permite que você use a função em uma declaração with, que é um tipo de gerenciador de contexto. Os gerenciadores de contexto garantem que os recursos sejam limpos corretamente, mesmo que ocorra um erro.

Quando você usa get_session em uma declaração with, como with get_session() as session:, o Python automaticamente:
- Chama a função get_session e inicia a sessão do banco de dados.
- Consome o primeiro item do gerador (a sessão do banco de dados) e o atribui à variável session.
- Executa o bloco de código dentro do with.
- Consome o restante do gerador (neste caso, não há mais itens a serem produzidos).
- Executa o bloco finally, fechando a sessão do banco de dados.

``` python
if __name__ == "__main__":
    create_tables()

    with get_session() as session:
        person = Person(name="John", age=30)
        session.add(person)
        session.commit()
        print("Person added successfully!")
```

Isso garante que a sessão do banco de dados seja sempre fechada corretamente, mesmo que ocorra um erro dentro do bloco with. Isso não seria possível se você usasse return em vez de yield.

### 1.4.2 Módulo core/infrastructure/orm/models
- Este módulo é responsável pela definição dos objetos que serão persistidos por meio do ORM;

# Aula 2: Repository pattern (Branch: feat/lesson-2-repo-pattern)

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