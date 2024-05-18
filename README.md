# Aula 1: ORM

## O que é um ORM?
Um ORM (Object-Relational Mapping) é uma técnica de programação que mapeia objetos definidos em uma linguagem de programação orientada a objetos para estruturas de dados em um banco de dados relacional. Isso permite que os desenvolvedores usem objetos e métodos orientados a objetos para interagir com o banco de dados, em vez de escrever consultas SQL diretamente.

## O que é o SQLAlchemy?
O SQLAlchemy é uma biblioteca de mapeamento objeto-relacional (ORM) para Python. Ele fornece uma maneira de mapear objetos Python para tabelas em um banco de dados relacional, facilitando o desenvolvimento de aplicativos que lidam com dados de maneira orientada a objetos. SQLAlchemy suporta uma variedade de bancos de dados SQL e oferece uma API flexível e poderosa para criar consultas, gerenciar transações e interagir com o banco de dados de forma programática.

## O que é necessário para executar o código da primeira aula?
- Acesse a branch **feat/lesson-1-orm** para verificar o código desta aula.

### Criação do ambiente virtual
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

### Instalação das dependências do projeto
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

### Criação do arquivo de variável de ambiente
Crie um arquivo .env na raíz do projeto e preencha de acordo com o .env.example.

### Execução do código
Em construção...