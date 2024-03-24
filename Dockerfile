FROM python:3.10.14-alpine3.18

# set work directory
WORKDIR /app

# copy requirements file
COPY ./requirements.txt /app/

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        openssl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /app/

# copy .env
COPY .env /app/

RUN python -c 'import os, dotenv; dotenv.load_dotenv(".env")'

# expose port
EXPOSE 3000

# run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
