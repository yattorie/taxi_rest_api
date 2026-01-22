FROM python:3.12-slim

# Говорим Python не создавать временные файлы (.pyc) - чтобы не захламлять контейнер
ENV PYTHONDONTWRITEBYTECODE=1

# Говорим Python сразу показывать все сообщения в консоли (без задержек)
ENV PYTHONUNBUFFERED=1

# Создаем папку /app внутри контейнера и переходим в нее
WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# copy project
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
