FROM python:3.11.6-alpine3.17

ENV SECRET_KEY=fdkjshfhjsdfdskfdsfdcbsjdkfdsdf
ENV APP_SETTINGS=config.TestingConfig
ENV DATABASE_URL=sqlite:///database.db
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_APP=src

COPY requirements.txt .
COPY c_compile.py .
COPY config.py .
COPY /src /src

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 gcc -shared -o src/static/c/bmp64lib.so -fPIC src/static/c/bmp64lib.c -O3 -Wno-unused-result && \
 apk --purge del .build-deps




RUN mkdir /instance

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /src && chmod -R u+rwx /src && chown -R appuser /instance && chmod -R u+rwx /instance
USER appuser

EXPOSE 8000


CMD ["gunicorn","src:app","-b", "0.0.0.0:8000"]
