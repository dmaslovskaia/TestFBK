FROM python:3.8.0-alpine as builder

# Prevent Python from writing pyc files to disc & from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app

COPY ./requirements.txt /opt/app/requirements.txt

# install psycopg2 & app dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /opt/app/wheels -r requirements.txt

FROM python:3.8.0-alpine

WORKDIR /opt/test_fbk

# Create special app user
RUN addgroup -S app && adduser -h /opt/test_fbk -D -S -G app app

COPY ./test /opt/test_fbk

# Install app dependencies
COPY --from=builder /opt/app/wheels ./test_fbk/wheels
RUN apk update && apk add libpq
RUN pip install --upgrade pip && pip install --no-cache ./test_fbk/wheels/*

RUN chown -R app:app /opt/test_fbk

USER app

ENTRYPOINT ["/opt/test_fbk/entrypoint.sh"]
