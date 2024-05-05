FROM python:3.10.11-slim-buster

RUN apt-get update && apt-get upgrade -y

RUN apt-get update \
    && apt-get upgrade \
    && apt-get install -y libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./main.py"]
