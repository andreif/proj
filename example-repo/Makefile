include local.env

PY = 3.9.0
PROJECT := example
SOURCE_COMMIT := $(shell git rev-parse HEAD)
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)

.DEFAULT_GOAL := help

.PHONY: help  # shows available commands
help: Makefile
	@echo "\nAvailable commands:\n"
	@sed -n 's/^.PHONY:\(.*\)/ *\1/p' $<
	@echo


.PHONY: build
build:
	docker-compose build --build-arg SOURCE_COMMIT=$(SOURCE_COMMIT) app
	docker-compose up -d app
	docker-compose logs -f --tail=200 app

.PHONY: logs
logs:
	docker-compose logs -f --tail=200 app


.PHONY: manage
manage:
	SOURCE_COMMIT=$(SOURCE_COMMIT) \
	pipenv run src/manage.py $(ARGS)
#env $(shell cat local.env | xargs) \


.PHONY: server
server:
	make manage runserver


.PHONY: task
task:
	pipenv run python src/$(PROJECT)/tasks.py $(ARGS)


.PHONY: requirements
requirements:
	pipenv lock --requirements > requirements.txt


.PHONY: setup
setup:
	pyenv install --skip-existing $(PY)
	pyenv local $(PY)
	pip install -U pip pipenv
	pipenv install --dev
	createdb $(PROJECT) || true
	test -e .env || ln -s local.env .env
	make manage migrate
	make manage createsuperuser


.PHONY: clean
clean:
	pipenv --rm || true
	dropdb $(PROJECT)


.PHONY: venv
venv:
	pipenv shell


.PHONY: version
version:
	heroku config:set SOURCE_COMMIT=$(shell git rev-parse --short master)


.PHONY: deploy
deploy:
	git push heroku master $(GIT_ARGS) 2>&1 | tee /dev/tty | grep "Verifying deploy... done."
	make version
	heroku logs


.PHONY: deploy-force
deploy-force:
	GIT_ARGS=--force make deploy
