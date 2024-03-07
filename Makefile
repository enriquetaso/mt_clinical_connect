###########################
##       Variables       ##
###########################
VERSION?=0.0.1
PYTHON_VERSION=python3

###########################
##       Commands        ##
###########################

init: 
	$(PYTHON_VERSION) -m venv venv
	venv/bin/pip install -r requirements.txt

format:
	venv/bin/black api/ core/
	venv/bin/ruff check api/ core/

run/devserver:
	venv/bin/python manage.py runserver

run/make_migrations:
	venv/bin/python manage.py makemigrations

run/migrate:
	venv/bin/python manage.py migrate

run/test:
	venv/bin/python manage.py test

build:
	docker compose build

start:
	docker compose up -d

clean:
	docker compose down

remove:
	docker compose down -v

makemigrations:
	docker compose run --rm app python manage.py makemigrations

migrate:
	docker compose run --rm app python manage.py migrate

test:
	docker compose run --rm app python manage.py test