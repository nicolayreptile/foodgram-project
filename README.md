# Foodgram Project - Продуктовый помощик

Link [https://foodgram.gq/](https://foodgram.gq/)

## About

Foodgram is a web project on Django Framework allowed publish recipes by users. Foodgram allows users adding recipes to favorites, following authors and creating shop list of ingredients into PDF.

## Installation

#### 1. Copy ***docker-compose.yaml*** in destination ***foodgram_project***.
#### 2. Create file ***.env*** with your environment variables. For example ***.env*** might look like this
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
DB_USER=foodgram
DB_PASSWORD=foodgram
DB_HOST=db
DB_PORT=5432
POSTGRES_USER=foodgram
POSTGRES_PASSWORD=foodgram
```
#### 3. Run command
```
docker-compose up -d
```
#### 4. Execute commands for create database scructure
```
docker exec -it foodgram_project_web_1 python manage.py makemigrations
```
```
docker exec -it foodgram_project_web_1 python manage.py migrate
```

#### 5. You can create your own superuser by run command
```
docker exec -it foodgram_project_web_1 python manage.py createsuperuser
```
#### 6. Finally
For any questions contact with me on Telegram @nicolay_reptile
