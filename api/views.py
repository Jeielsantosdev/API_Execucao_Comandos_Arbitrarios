import os
import subprocess
from ninja import Router
from ninja.security import HttpBearer
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from ninja.responses import Response
from ninja.pagination import paginate
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .schemas import *
from .models import *
from .pagination import SafePagination

router = Router()

# JWT Authentication
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256']
            )
            return payload
        except jwt.InvalidTokenError:
            return None


@router.post('/auth/token/')
def get_token(request, data: AuthSchema):

    user = authenticate(
        request, username=data.username, password=data.password
    )
    if user is not None:
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return {'token': token}
    else:
        return Response(
            {'detail': 'Invalid credentials'}, status=401
        )


@router.post('/execute/', response=ExecuteOutput, auth=AuthBearer())
def execute_command(request, data: ExecuteInput):
    # validação de segurança
    bin_path = os.path.join('./bin', data.binary)
    if not os.path.isfile(bin_path) or not os.access(bin_path, os.X_OK):
        return Response({"erro":"Binary not found or not executable"}, status=404)

    # Prevenir path traversal
    if '..' in data.command or '/' in data.binary:
        return Response({"erro":"Invalid  binary path"}, status=400)

    # montar o comando
    cmd = [bin_path, data.command] + data.args
    try:
        # executar comando
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        )
        # Preservar caracteres de escape
        stdout = result.stdout.encode('unicode_escape').decode('utf-8')
        stderr = result.stderr.encode('unicode_escape').decode('utf-8')

        # Cria log
        log_entry = Executionlog.objects.create(
            binary=data.binary,
            command=data.command,
            args=data.args,
            stdout=stdout,
            stderr=stderr,
            status_code=result.returncode,
        )

        # formatar o log para a resposta
        log_str = (
            f'{log_entry.timestamp.isoformat()} | '
            f"./bin/{log_entry.binary} {log_entry.command} {' '.join(log_entry.args)} | "
            f'STDOUT: {stdout} | STDERR: {stderr}'
        )

        return {
            'status_code': result.returncode,
            'stdout': stdout,
            'stderr': stderr,
            'log': log_str,
        }
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else 'Erro desconhecido'
        raise HttpError(400, f'Execução falhou: {stderr}')
    except Exception as e:
        raise HttpError(500, "Arquivo '.bin/busybox' não encontrado")



@router.get('/logs/', response=List[LogOutput], auth=AuthBearer())
@paginate(SafePagination)
def get_logs(request):
    return Executionlog.objects.all().order_by('-timestamp')