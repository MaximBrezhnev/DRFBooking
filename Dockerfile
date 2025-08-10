FROM python:3.12

RUN mkdir app
WORKDIR /app

RUN pip install --upgrade pip setuptools wheel

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock /app/

ARG ENV

RUN if [ "$ENV" = "development" ]; then \
    	poetry install --with dev,test; \
    elif [ "$ENV" = "test" ]; then \
      	poetry install --with test; \
    fi

COPY . .