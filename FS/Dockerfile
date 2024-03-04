# Dockerfile for Fibonacci Server
FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 9090

CMD ["python", "fibonacci_server.py"]
