# API de Execução de Comandos Arbitrários

API REST segura para executar binários locais arbitrários dentro da pasta `./bin/` protegida por autenticação JWT. 

---

## Tecnologias

- Python 3.12
- Django 4.x
- Django Ninja (API REST)
- PostgreSQL
- Docker e Docker Compose
- JWT para autenticação

---

## Funcionalidades

- Execução controlada de binários locais (`./bin/`) via API
- Validação contra Path Traversal
- Prevenção de injeção de comandos (uso de `subprocess.run` com `shell=False`)
- Verificação de permissões de execução nos binários
- Autenticação via JWT para proteger todos os endpoints
- Scripts para setup automático do ambiente via Docker

---

## Pré-requisitos

- Docker e Docker Compose instalados
- Git
- postman, curl(ou qualquer outra ferramenta usavel para o teste)

---

## Instalação e Setup

1. Clone o repositório:
   ```bash
   git clone https://github.com/Jeielsantosdev/API_Execucao_Comandos_Arbitrarios.git
   cd API_Execucao_Comandos_Arbitrarios

2. Construa e suba o ambiente Docker
    docker-compose up --build -d
3. Execute as migrations
    docker-compose exec app python manage.py migrate

3. Execute o script de setup para aplicar migrations e criar superusuário:
    docker-compose exec app bash setup.sh

4. Endpoints

* **POST** — Executa o comando.
### `http://localhost:800/api/auth/token/`
* Payload:
    ```json
    curl -X POST http://localhost:8000/api/auth/token/ \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "admin#2023"}'

    
    ```
* Response
    ```json
    {
    "token": "<TOKEN>"
    }
    
    ```

### `http://localhost:8000/api/execute/`

* **POST** — Executa o comando.
* Payload:

   ```
    curl -X POST http://localhost:8000/api/execute/ \
    -H "Authorization: Bearer <TOKEN>" \
    -H "Content-Type: application/json" \
    -d '{
    "binary": "busybox",
    "command": "ls",
    "args": ["-la", "/"]
    }'

    ```


### `http://localhost:8000/api/logs/`

* **GET** — Lista os últimos logs de execução, com paginação opcional.
    curl -X GET http://localhost:8000/api/logs/ \
     -H "Authorization: Bearer <TOKEN>"
