FROM python:3.9.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN mkdir /local
RUN python -m venv /local/venv
RUN /local/venv/bin/pip install --upgrade pip
RUN /local/venv/bin/pip install -r requirements.txt

COPY . /app/

CMD . /local/venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000