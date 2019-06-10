# https://medium.com/locust-io-experiments/locust-io-experiments-running-in-docker-cae3c7f9386e

# FROM python:3.6-alpine
FROM python:3

COPY /docker-entrypoint.sh /
COPY /requirements.txt /

RUN pip install -r requirements.txt \
    && chmod +x /docker-entrypoint.sh

RUN  mkdir /locust
WORKDIR /locust
EXPOSE 8089 5557 5558

ENTRYPOINT ["/docker-entrypoint.sh"]
