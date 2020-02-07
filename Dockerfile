FROM python:3.7-alpine

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=Europe/London
RUN apk add --update --no-cache tzdata

RUN pip install --no-cache-dir poetry && \
    poetry config settings.virtualenvs.create false

WORKDIR /opt/api
COPY *.toml *.lock ./
RUN apk --update add --no-cache build-base linux-headers git libffi-dev openssl-dev && \
    poetry install --no-interaction --no-dev

RUN addgroup -S app && \
    adduser -SD -G app -s /bin/ash app

COPY ./ ./

ENV IS_DOCKER=1 PRODUCTION=1 PYTHONPATH=/opt/api
ENV SERVER_WORKERS=1 SERVER_PORT=7474
CMD python -m sanic autoapp.app --host=0.0.0.0 --port=${SERVER_PORT} --workers=${SERVER_WORKERS}
