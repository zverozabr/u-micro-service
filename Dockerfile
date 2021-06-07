FROM python:3.9.2
USER root

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1


WORKDIR /app
COPY . /app

RUN pip install pipenv && pipenv install --system --deploy --skip-lock && pipenv install ujson

CMD ["pipenv", "run", "python", "app.py"]
