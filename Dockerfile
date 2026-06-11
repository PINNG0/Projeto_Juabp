# Usa uma imagem oficial do Python super leve e rápida
FROM python:3.11

# Cria uma pasta chamada /app dentro do servidor virtual
WORKDIR /app

# Copia todos os seus arquivos do PC para dentro do servidor
COPY . .

# Instala o Flask e outras coisas que estiverem no requirements.txt
RUN pip install -r requirements.txt

# O comando que ele roda para ligar o site
CMD ["python", "app/main.py"]
