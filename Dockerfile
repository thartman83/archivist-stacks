FROM python:3.11-slim-bullseye

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql \
    && rm -rf /var/lib/apt/lists/*

#RUN git clone --depth 1 --branch main https://github.com/thartman83/archivist-descry.git /app
COPY requirements-dev.txt /
RUN pip3 install -r /requirements-dev.txt

COPY . .

ENV APPCONFIG PROD

CMD [ "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80" ]
