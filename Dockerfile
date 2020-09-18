FROM python:3.6

WORKDIR /code

COPY . .

RUN apt update
RUN apt install fonts-freefont-ttf -y
RUN pip install -r /code/requirements.txt

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
LABEL author=timofey_abonosimov
