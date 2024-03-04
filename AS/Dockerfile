# Dockerfile for Authoritative Server
FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 53533/udp

CMD ["python", "authoritative_server.py"]
