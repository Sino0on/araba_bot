# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY . .

# Устанавливаем переменную окружения для запуска aiogram
ENV PYTHONUNBUFFERED=1

# Запускаем бота
CMD ["python", "bot.py"]