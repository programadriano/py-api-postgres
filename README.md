# Projeto Flask com PostgreSQL

Este projeto demonstra como criar uma aplicação Flask que utiliza PostgreSQL como banco de dados.

## Configuração do Ambiente
Primeiro, crie um ambiente virtual para isolar as dependências do projeto:

```shell
python -m venv envs
```

Ative o ambiente virtual:

* No Windows:
```shell
envs\Scripts\activate.bat
```

* No Unix ou macOS:
```shell
source envs/bin/activate
```

## Instalar Dependências
Com o ambiente virtual ativado, instale as dependências necessárias:

```shell
pip install flask sqlalchemy psycopg2-binary flask_sqlalchemy flask-restx
```

## Configuração do Banco de Dados

Inicie uma instância do PostgreSQL usando Docker:

```shell
docker run --name db_local -e POSTGRES_PASSWORD=102030 -d -p 5432:5432 postgres
```

Isso criará e iniciará um contêiner Docker chamado db_local rodando PostgreSQL. A porta 5432 do contêiner será mapeada para a porta 5432 do host.

## Criar a Tabela usuario
Conecte-se ao banco de dados PostgreSQL (você pode usar o psql ou uma ferramenta GUI como pgAdmin) e execute o seguinte comando SQL para criar a tabela usuario:

```shell
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE
);
```

## Executar a Aplicação
Com o ambiente configurado e o banco de dados iniciado, você pode agora executar sua aplicação Flask com o comando 
`python main.py`