FROM python:3.6

WORKDIR /code

COPY . .

RUN pip install -r /code/requirements.txt

RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations --noinput

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
LABEL author=timofey_abonosimov
