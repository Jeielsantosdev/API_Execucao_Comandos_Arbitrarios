#!/bin/bash

# Parar script em caso de erro
set -e

echo "🗂️  Aplicando migrações..."
python manage.py migrate

# Verifica se o superusuário já existe
echo "👤 Criando superusuário..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin#2023")
    print("✅ Superusuário criado com sucesso!")
else:
    print("ℹ️  Superusuário já existe.")
END
