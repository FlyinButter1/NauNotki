FROM python:3.12-alpine3.17

ENV SECRET_KEY=fdkjshfhjsdfdskfdsfdcbsjdkfdsdf
ENV APP_SETTINGS=config.TestingConfig
ENV DATABASE_URL=sqlite:///database.db
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_APP=src

RUN apk add build-base

COPY requirements.txt .
RUN python -m pip install -r requirements.txt


COPY config.py .
COPY /src /src

RUN mkdir /instance

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /src && chmod -R u+rwx /src && chown -R appuser /instance && chmod -R u+rwx /instance
USER appuser

EXPOSE 8000


CMD ["gunicorn","src:app","-b", "0.0.0.0:8000"]
