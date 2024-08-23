FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код приложения
COPY . .

# Устанавливаем команду по умолчанию для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]