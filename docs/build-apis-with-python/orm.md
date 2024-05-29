# 1 - ORM
O código desta aula está disponível na branch indicada abaixo:
- [(Branch: feat/lesson-1-orm)](https://github.com/kvojps/learn-programming/tree/feat/lesson-1-orm)

## 1.1 O que é um ORM?
Um ORM (Object-Relational Mapping) é uma técnica de programação que mapeia objetos definidos em uma linguagem de programação orientada a objetos para estruturas de dados em um banco de dados relacional. Isso permite que os desenvolvedores usem objetos e métodos orientados a objetos para interagir com o banco de dados, em vez de escrever consultas SQL diretamente.

## 1.2 O que é o SQLAlchemy?
O SQLAlchemy é uma biblioteca de mapeamento objeto-relacional (ORM) para Python. Ele fornece uma maneira de mapear objetos Python para tabelas em um banco de dados relacional, facilitando o desenvolvimento de aplicativos que lidam com dados de maneira orientada a objetos. SQLAlchemy suporta uma variedade de bancos de dados SQL e oferece uma API flexível e poderosa para criar consultas, gerenciar transações e interagir com o banco de dados de forma programática.

## 1.3 Configuração do SQLAlchemy no projeto

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

### 1.3.4 Definição do módulo core/infrastructure/settings
- O módulo settings é responsável pelas configurações necessárias para acessar recursos externos;
- O arquivo **env_handler.py** é responsável pela obtenção de váriaveis de ambiente presentes no arquivo .env;
- O arquivo **db.py** é responsável por:
    - Realizar a conexão com o banco de dados;
    - Criar uma sessão com o banco de dados;
    - Definir a classe Base do ORM SQLAlchemy que serão utilizadas por todas as classes que serão persistidas no banco de dados;

### 1.3.5 Obter sessão com o banco de dados

```python
@contextmanager
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

### 1.3.6 Módulo core/infrastructure/orm/models
- Este módulo é responsável pela definição dos objetos que serão persistidos por meio do ORM;

### 1.3.7 Execução do código
- Execute o arquivo **main.py** na raíz do projeto;
  - Este arquivo executa uma inserção de dados no banco de dados por meio dos artefados construídos nessa aula;
