FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get -y install git locales locales-all


COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app.

CMD ["gunicorn", "fajne_dane.wsgi", "--bind", "0.0.0.0:80", "--workers", "2", "--worker-class", "gevent", "--access-logfile=-"]

EXPOSE 80

