## Hardcoded de usuários e senhas

### docker-compose.yml

As credenciais do banco estão **hardcoded** no `docker-compose.yml`, o que viola boas práticas de segurança. Isso facilita o vazamento de credenciais em repositórios públicos ou logs.

```yaml
environment:
  - POSTGRES_USER=user
  - POSTGRES_PASSWORD=J#20e07sz
  - POSTGRES_DB=dbarbitrarios
```

As variáveis de ambiente deveriam ser lidas de um `.env` seguro, ignorado pelo controle de versão (`.gitignore`), e referenciadas via `env_file` no `docker-compose.yml`.

### settings.py ignora o uso de variáveis de ambiente

As credenciais são repetidas e hardcoded diretamente no `settings.py`, sem uso do `.env`.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbarbitrarios',
        'USER': 'user',
        'PASSWORD': 'J#20e07sz',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

Deve-se utilizar `os.getenv` ou pacotes como `python-decouple` ou `django-environ` para carregar as variáveis sensíveis a partir de um arquivo `.env`.

## Criação de superusuário com mistura incorreta de shell script e Python

A criação do superusuário está sendo feita com uma abordagem mista e inconsistente entre **shell script e execução de Python embutido**, o que gera acoplamento indevido entre ambiente e lógica de negócio. Isso deve ser substituído por um **custom command** Django usando `BaseCommand`, garantindo controle, reutilização e validação explícita.

## Erro não tratado ao fornecer credenciais inválidas

A falha na autenticação não gera resposta HTTP adequada. O erro resulta em exceção do tipo `TypeError` devido a um `dict` como chave não hashable, expondo internamente o framework.

```python
Error: Internal Server Error
Response body

Traceback (most recent call last):
  File "/usr/local/lib/python3.12/site-packages/ninja/operation.py", line 134, in run
    return self._result_to_response(request, result, temporal_response)
  File "/usr/local/lib/python3.12/site-packages/ninja/operation.py", line 257, in _result_to_response
    if status in self.response_models:
TypeError: unhashable type: 'dict'
```

O retorno da view está violando o contrato de resposta esperado pelo **Django Ninja**, retornando um `dict` diretamente como `status code`, o que é inválido. Isso deve ser interceptado com `try/except` e retorno explícito de `HttpResponse` ou `HttpError` com código HTTP definido.

## Endpoint de logs não possui autenticação e paginação manual

O endpoint `/logs/` expõe uma lista potencialmente massiva de registros sem controle de acesso e sem paginação. Isso pode comprometer a segurança e estabilidade do sistema.

```python
@router.get('/logs/', response=List[LogOutput])
```

Não há autenticação com `@router.auth()` nem controle de paginação com o decorador `@paginate()`. Isso permite **enumeração massiva de dados**, além de possível exfiltração de logs sensíveis. Além disso, a ausência de `LIMIT` pode causar erro grave caso o offset seja muito alto.

Se `offset` ultrapassar o limite do tipo `bigint`, ocorre:

```python
Traceback (most recent call last):
  File "/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
psycopg2.errors.NumericValueOutOfRange: bigint out of range
```

Isso é resultado direto da falta de validação no valor de entrada. O backend deve sanitizar entradas e limitar offsets de forma explícita. Além disso, o uso de `paginator.paginate_queryset` do Django REST Framework ou `@paginate()` do Django Ninja evita o problema. O endpoint deve exigir autenticação e utilizar `QueryParams` validados com ranges máximos definidos.


## Toda a lógica do endpoint `/logs/` é um desastre em segurança e performance

Esse é, objetivamente, o pior tipo de paginação possível.

```python
queryset = Executionlog.objects.all().order_by('-timestamp')[
    offset : offset + limit
]
for log in queryset:
    logs.append(
        LogOutput(
            id=log.id,
            timestamp=log.timestamp,
            binary=log.binary,
            command=log.command,
            args=log.args,
            stdout=log.stdout,
            stderr=log.stderr,
            status_code=log.status_code,
        )
    )
return logs
```




