FROM python:3

COPY /docker-entrypoint.sh /
COPY /requirements.txt /

RUN pip install -r requirements.txt \
    && chmod +x /docker-entrypoint.sh

RUN  mkdir /locust
WORKDIR /locust
EXPOSE 8089 5557 5558

ENTRYPOINT ["/docker-entrypoint.sh"]
