FROM python:3.10

COPY . .

RUN pip install -U pip
RUN pip install -r requirements.txt
ADD data/init.sql /docker-entrypoint-initdb.d
