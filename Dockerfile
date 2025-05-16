# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

# WORKDIR /app

# EXPOSE 80

# COPY requirements.txt .

# RUN ["pip", "install", "-r","./requirements.txt"]

# COPY . .

# CMD ["python3","main.py"]




FROM python:3.12-slim


WORKDIR /app


COPY ./requirements.txt .


RUN ["pip", "install", "-r","./requirements.txt"]

COPY ./app /app
COPY ./src /app/src

CMD ["fastapi", "run", "main.py", "--port", "8000"]
