# Sumário
- [Aula 1: ORM (Branch: feat/lesson-1-orm)](#aula-1-orm-branch-featlesson-1-orm)
- [Aula 2: Repository pattern (Branch: feat/lesson-2-repo-pattern)](#aula-2-repository-pattern-branch-featlesson-2-repo-pattern)
- [Apêndices](#apêndices)
  - [Melhores práticas no design de REST APIs](#melhores-práticas-no-design-de-rest-apis)

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

# Apêndices
Nesta seção estão os conteúdos que ainda não possuem uma posição no fluxo de aulas.

## Melhores práticas no design de Rest APIs
### URI 
- **Substantivos:** Use substantivos nas URIs para identificar claramente os recursos. Evite verbos, pois as URIs devem representar recursos e não ações. Por exemplo, em vez de **/getUser** use **/users**.
- **Plural:** Utilize o plural para nomear os recursos nas URIs, mesmo que o recurso possa ser único em determinadas operações. Isso torna a nomenclatura consistente e intuitiva. Por exemplo, **/users** em vez de **/user.**
- **Nest resources:** Utilize a aninhamento de recursos (nested resources) para representar a hierarquia e a relação entre recursos. Isso ajuda a organizar e a clarificar a estrutura da API. Por exemplo, para acessar os pedidos de um usuário específico, utilize **/users/{userId}/orders** em vez de algo como **/orders?userId={userId}**;
- **Consistência:** Mantenha consistência na estrutura e no estilo das URIs em toda a API. Isso inclui o uso consistente de maiúsculas/minúsculas, hifens, barras e pluralidade. Isso melhora a previsibilidade e a compreensão da API. Por exemplo, se você começar com **/users**, continue usando essa estrutura para outros recursos, como **/products** e **/categories**;
- **Versioning:** Inclua a versão da API na URI para permitir atualizações e mudanças sem quebrar a compatibilidade com versões anteriores. Isso pode ser feito utilizando um prefixo como /v1, /v2, etc. Por exemplo, /v1/users permite identificar claramente que está utilizando a versão 1 da API.

### Métodos HTTP
- **GET:**
  - **Conjunto de recursos:** Ao obter uma coleção de recursos, você pode aplicar paginação, filtragem e ordenação para controlar o volume e a organização dos dados retornados.
  - **Único recurso:** Solicita um único recurso específico por ID ou identificador único.
  - **Request:**
    - **Headers:** Pode incluir cabeçalhos para controle de cache, como `If-None-Match` ou `If-Modified-Since`.
    - **Body:** Não possui corpo na solicitação GET.

  - **Response:**
    - **Headers:** Pode incluir cabeçalhos para controle de cache, como `ETag` ou `Last-Modified`.
    - **Status code:** 
      - `200 OK`: Quando a solicitação é bem-sucedida e os dados são retornados.
      - `304 Not Modified`: Quando o recurso não foi modificado desde a última solicitação, com base nos cabeçalhos de cache.

- **POST:** Utilizado para criar um novo recurso em uma coleção. A URI alvo geralmente representa a coleção, e o novo recurso é adicionado a esta coleção. Pode ser usado para iniciar uma ação ou processamento específico em um recurso existente.
  - **Request:**
    - **Headers:** Pode incluir cabeçalhos como `Content-Type` para indicar o formato dos dados enviados.
    - **Body:** Inclui o corpo da solicitação com os dados do novo recurso a ser criado ou os parâmetros necessários para a ação a ser iniciada.

  - **Response:**
    - **Headers:** Pode incluir o cabeçalho `Location` indicando a URI do novo recurso criado.
    - **Status code:** 
      - `201 Created`: Quando um novo recurso é criado com sucesso.
      - `202 Accepted`: Quando a solicitação foi aceita para processamento, mas o processamento não foi concluído. Isso é útil para operações assíncronas, onde o cliente não precisa esperar a conclusão do processamento.

- **PUT:** O método PUT é utilizado para criar ou atualizar um recurso específico.
  - **Request:**
    - **Headers:** Pode incluir cabeçalhos como `If-Match` para controle de versões do recurso.
    - **Body:** Deve incluir o recurso completo a ser criado ou atualizado.
  - **Response:**
    - **Headers:** Pode incluir o cabeçalho `Location` indicando a URI do recurso criado ou atualizado.
    - **Status code:**
      - `201 Created`: Quando um novo recurso é criado com sucesso.
      - `200 OK`: Quando um recurso existente é atualizado com sucesso.
      - `204 No Content`: Quando um recurso existente é atualizado com sucesso e não há conteúdo adicional para retornar.
      - `404 Not Found`: Quando o recurso a ser atualizado não é encontrado.
      - `412 Precondition Failed`: Quando a condição especificada nos cabeçalhos, como `If-Match`, falha.

- **DELETE:**
  - **Request:**
    - **Headers:** Pode incluir cabeçalhos como `If-Match` para controle de versões do recurso.
    - **Body:** Não possui corpo na solicitação DELETE.

  - **Response:**
    - **Headers:** Nenhum cabeçalho específico necessário.
    - **Status code:**
      - `204 No Content`: Quando o recurso é removido com sucesso.
      - `412 Precondition Failed`: Quando a condição especificada nos cabeçalhos, como `If-Match`, falha.

### Idempontência
Idempontência refere-se a uma propriedade dos métodos HTTP que garante que realizar a mesma operação múltiplas vezes tenha o mesmo efeito que realizá-la apenas uma vez. Isso é importante para garantir a consistência e previsibilidade das operações na API.

- **GET:** Idempotente. Repetir a solicitação não altera o estado do recurso.
- **PUT:** Idempotente. Repetir a solicitação com os mesmos dados resulta no mesmo estado do recurso.
- **DELETE:** Idempotente. Repetir a solicitação para um recurso já deletado não altera o estado (continua deletado).
- **POST:** Não idempotente. Repetir a solicitação pode resultar na criação de novos recursos duplicados.

### Gerenciamento de Erros
- **4xx: Erros do Cliente** - Ocorrências que indicam que o cliente fez uma solicitação inválida ou incorreta.
- **5xx: Erros do Servidor** - Problemas que surgem devido a falhas no servidor ao processar uma solicitação válida.

### Saiba mais
O conteúdo desta seção foi baseado neste [vídeo.](https://youtu.be/A8t5LSxVJFM?si=3oOuNukYGu-mvg7b)