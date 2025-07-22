FROM python:3.12

RUN mkdir app
WORKDIR /app

RUN pip install --upgrade pip setuptools wheel

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock /app/

ARG ENV

RUN if [ "$ENV" = "prod" ]; then \
    	poetry install --no-root; \
  	elif [ "$ENV" = "local" ]; then \
    	poetry install --no-root --with local,test; \
    elif [ "$ENV" = "test" ]; then \
      	poetry install --no-root --with test; \
    fi

COPY . .