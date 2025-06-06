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

---

## Instalação e Setup

1. Clone o repositório:
   ```bash
   git clone https://github.com/Jeielsantosdev/API_Execucao_Comandos_Arbitrarios.git
   cd API_Execucao_Comandos_Arbitrarios

2. Construa e suba o ambiente Docker
    docker-compose up --build -d
3. Execute o script de setup para aplicar migrations e criar superusuário:
    docker-compose exec app bash setup.sh
