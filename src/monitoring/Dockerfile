FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "monitoring_task.py"]