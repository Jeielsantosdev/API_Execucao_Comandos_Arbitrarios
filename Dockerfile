# Usa a imagem oficial do Python como base
FROM python:3.12

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependência primeiro para aproveitar cache
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o diretório de trabalho
COPY . .

# Expõe a porta usada pelo Gunicorn
EXPOSE 8000

# Comando de inicialização do Gunicorn com caminho correto do WSGI
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
