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

WORKDIR /opt/project

# Create special app user
RUN addgroup -S app && adduser -h /opt/project -D -S -G app app

COPY ./project /opt/project

# Install app dependencies
COPY --from=builder /opt/app/wheels ./project/wheels
RUN apk update && apk add libpq
RUN pip install --upgrade pip && pip install --no-cache ./project/wheels/*

RUN chown -R app:app /opt/project

USER app

ENTRYPOINT ["/opt/project/entrypoint.sh"]
