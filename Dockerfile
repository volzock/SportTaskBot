FROM python:3.12-slim

RUN mkdir -p /code
WORKDIR /code
COPY . /code
ENV BOT_TOKEN=


RUN pip install poetry
RUN poetry install
EXPOSE 5432

CMD ["poetry", "run", "python", "bot/main.py"]