# API RESTful Curso

Este é um projeto de API RESTful desenvolvido com Flask para um curso. A API permite a criação, leitura, atualização e exclusão de usuários, posts e roles.

## Estrutura do Projeto
.env .pytest_cache/ apirestfull_curso/ init.py src/ pycache/ app.py config.py controllers/ models/ utils.py views/ tests/ env/ instance/ migrations/ poetry.lock Procfile pyproject.toml README.md

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

#### Desenvolvimento
  ```
  $ENVIRONMENT=development DATABASE_URL=postgresql+psycopg://<usuario>:<senha>@<host>/<database> JWT_SECRET_KEY="super-secret"
  ```
#### Teste
  ```
  $ENVIRONMENT=testing DATABASE_URL=postgresql+psycopg://<usuario>:<senha>@<host>/<database> JWT_SECRET_KEY="super-secret"
  ```
#### Produção
  ```
  $ENVIRONMENT=production DATABASE_URL=postgresql+psycopg://<usuario>:<senha>@<host>/<database> JWT_SECRET_KEY="super-secret"
  ```
### Instalação

```
1. Clone o repositório:

git clone <url-do-repositorio>
cd apirestfull_curso

2. Crie e ative um ambiente virtual:

python -m venv env
source env/bin/activate  # No Windows use `env\Scripts\activate`

3. Instale as dependências:

pip install poetry
poetry install
```

### Migrações do Banco de Dados

```
 1. Inicialize o banco de dados:

  poetry run flask --app apirestfull_curso.src.app db init
  poetry run flask --app apirestfull_curso.src.app -m "Initial migration."
  poetry run flask --app apirestfull_curso.src.app db upgrade
```
### Executando a Aplicação
```
Para iniciar a aplicação, execute:
    $env:ENVIRONMENT="development"; poetry run flask --app apirestfull_curso.src.app run --debug

Testes
  Para rodar os testes, use:
    $env:ENVIRONMENT="testing"; pytest apirestfull_curso/tests

```
## Estrutura de Diretórios

- `app.py`: Arquivo principal da aplicação Flask.
- `config.py`: Configurações da aplicação.
- `controllers`: Controladores para as rotas da API.
- `models`: Modelos do banco de dados.
- `utils.py`: Funções utilitárias.
- `views`: Schemas para serialização/deserialização.
- `tests`: Testes unitários e de integração.

## Endpoints

### Autenticação

- `POST /auth/login`: Autenticação de usuário.

### Usuários

- `POST /users/created`: Criação de usuário.
- `GET /users/list`: Listagem de usuários.
- `GET /users/get/<int:user_id>`: Obter usuário por ID.
- `PATCH /users/update/<int:user_id>`: Atualizar usuário por ID.
- `DELETE /users/delete/<int:user_id>`: Deletar usuário por ID.

### Posts

- `POST /posts/create`: Criação de post.
- `GET /posts/list`: Listagem de posts.
- `GET /posts/get/<int:post_id>`: Obter post por ID.
- `PATCH /posts/update/<int:post_id>`: Atualizar post por ID.
- `DELETE /posts/delete/<int:post_id>`: Deletar post por ID.

### Roles

- `POST /roles/created`: Criação de role.
- `GET /roles/list`: Listagem de roles.
- `GET /roles/get/<int:role_id>`: Obter role por ID.
- `DELETE /roles/delete/<int:role_id>`: Deletar role por ID.

