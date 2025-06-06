## Teste Técnico — API de Execução de Comandos Arbitrários

### Descrição Geral

O objetivo deste teste é construir uma **API REST** utilizando **Django Ninja**, protegida com **JWT**, capaz de executar **comandos arbitrários** utilizando **binários locais** armazenados na pasta **`./bin/`** na raiz do projeto. Esses binários podem incluir **`busybox`**, **`uutils`** (ou qualquer outro coreutils compilado).

A API deverá aceitar um comando e seus argumentos, executar esse comando via subprocess diretamente no sistema host, e retornar:

* **stdout** (preservando caracteres de escape como `\n`, `\t`, `\r`)
* **stderr** (com o mesmo critério)
* **status code** da execução (exit code do processo)

Além disso, toda execução deverá ser logada, incluindo:

* Timestamp
* Comando executado (com argumentos)
* stdout e stderr (com os caracteres de escape preservados)
* status code

O ambiente deve ser provisionado via **Docker**, mas a execução dos binários ocorre diretamente no sistema do container, sem uso de containers adicionais.

---

## Stack Obrigatória

* **Python (>=3.10)**
* **Django**
* **Django Ninja**
* **PostgreSQL ou SQLite**
* **Docker**
* **Binários locais:**

  * **`./bin/busybox`**
  * **`./bin/uutils`** (ou outro coreutils alternativo)

---

## Requisitos Funcionais

### API `/api/execute/`

* **Método:** `POST`
* **Autenticação:** JWT obrigatória

### Payload de entrada:

```json
{
  "binary": "busybox",
  "command": "ls",
  "args": ["-la", "/"]
}
```

### Resposta esperada:

```json
{
  "status_code": 0,
  "stdout": "bin\nboot\ndev\netc\n...",
  "stderr": "",
  "log": "2025-06-04T13:00:00Z | ./bin/busybox ls -la / | STDOUT: bin\\nboot\\ndev\\netc\\n... | STDERR: "
}
```

### Regras obrigatórias:

* O campo **`binary`** corresponde exatamente ao nome do executável presente em `./bin/`.
* O backend executará apenas binários presentes na pasta `./bin/`. Se o binário não existir ou não tiver permissão de execução, retorna erro HTTP 400.
* O campo **`command`** é o subcomando passado para o binário. Exemplo: para `busybox ls -la`, `ls` é o subcomando.
* O campo **`args`** é uma lista de argumentos adicionais passados para o subcomando.
* A API monta o comando final assim:

```bash
./bin/{binary} {command} {args...}
```

* O parser e executor devem capturar stdout, stderr e status code.
* Caracteres de escape devem ser preservados na saída, tanto no retorno JSON quanto no log.
* Logs devem ser armazenados no banco com: timestamp, comando completo, stdout e stderr.

---

## Regras de Segurança

* Não é permitido executar comandos externos fora de `./bin/`.
* Tentativas de path traversal (ex: `../../bin/sh`) são bloqueadas.
* O backend valida que o binário existe fisicamente e possui permissão de execução antes de executar.
* A execução é bloqueada caso o binário não esteja na lista permitida (`./bin/`).


---

## Endpoints

### `/auth/token`

* **POST** — Login com usuário e senha, retorna JWT.

### `/api/execute/`

* **POST** — Executa o comando.
* Payload:

```json
{
  "binary": "busybox",
  "command": "ls",
  "args": ["-la", "/"]
}
```

* Response:

```json
{
  "status_code": 0,
  "stdout": "output...\n",
  "stderr": "error output if any\n",
  "log": "2025-06-04T13:00:00Z | ./bin/busybox ls -la / | STDOUT: output...\\n | STDERR: error output if any\\n"
}
```

### `/api/logs/`

* **GET** — Lista os últimos logs de execução, com paginação opcional.

---

## Estrutura Esperada no Banco

### Model `ExecutionLog`:

* id
* timestamp
* binary (string)
* command (string)
* args (json)
* stdout (text)
* stderr (text)
* status\_code (integer)

---

## Docker

* O projeto deve ter um `Dockerfile` que provisiona o ambiente Python e Django.
* A pasta `./bin/` deve ser criada e os binários (`busybox`, `uutils`, etc.) devem ser copiados para ela com permissão de execução (`chmod +x`).
* O docker-compose deve subir o serviço Django e o banco (PostgreSQL ou SQLite).

---

## Regras Críticas de Implementação

* O executor deve usar subprocess com shell=False, protegendo contra injeções.
* Saídas precisam ser codificadas para preservar exatamente os caracteres de escape. Exemplo:

```plaintext
line1\nline2\titem
```

Deve ser representado no JSON como:

```json
"line1\\nline2\\titem"
```

* Logs precisam refletir exatamente a execução, inclusive stderr mesmo quando vazio.
* Erros como binário inexistente, permissão negada, ou falha no subprocess, devem gerar respostas HTTP 400 ou 500 adequadas, com mensagens claras.

---

## Entregáveis

* Projeto Django completo
* Dockerfile e docker-compose operacionais
* Scripts para setup inicial (criação de usuário admin, migrações, etc.)
* README contendo:

  * Setup
  * Rodar a API via docker-compose
  * Exemplos de uso dos endpoints (curl, httpie, ou outro)

