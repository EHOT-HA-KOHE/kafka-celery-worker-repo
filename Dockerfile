FROM python:3.12-slim

# Устанавливаем зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Копируем consumer.py в рабочую директорию
COPY . /app
WORKDIR /app

# Команда по умолчанию
CMD ["python", "consumer.py"]
