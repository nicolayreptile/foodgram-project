FROM python:3.6

RUN mkdir /code

COPY . /code

RUN pip install -r /code/requirements.txt

WORKDIR /code

RUN python manage.py collectstatic --noinput
#RUN python manage.py makemigrations --noinput
#RUN python manage.py migrate --noinput

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
LABEL author=timofey_abonosimov
