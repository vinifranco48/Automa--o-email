# Use uma imagem base do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
COPY app.py .

# Instala as bibliotecas necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Define variáveis de ambiente (você pode sobrescrevê-las ao executar o contêiner)
ENV SENDER_EMAIL=viniabreu48@gmail.com
ENV SENDER_PASSWORD=nzbxlalkxvbkbmyo

# Comando para rodar o script Python
CMD ["python", "app.py"]