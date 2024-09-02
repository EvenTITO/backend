FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y git

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r  /code/requirements.txt && \
    rm -rf /root/.cache /var/lib/apt/lists/* /tmp/*

RUN apt-get remove -y git && apt-get autoremove -y

COPY ./app /code/app

CMD uvicorn app.main:app --host=0.0.0.0 --port=${PORT}
