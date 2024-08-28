FROM python:3.8-slim

WORKDIR /Docker 

COPY . /Docker

CMD ["python", "script.py"]
