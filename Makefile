SHELL := /bin/bash
VENV_PATH=./.venv/bin/activate
ENVIRONMENT_VARIABLE_FILE=./.env

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help:
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)

freeze: ## updates the requirements.txt file
	pip freeze > requirements.txt

install: ## installs requirements
install:
	pip install -r requirements.txt

env: ## Source venv and environment files for testing
env:
	python3 -m venv .venv
	source $(VENV_PATH)
	source $(ENVIRONMENT_VARIABLE_FILE)

init: ## sets up environment and installs requirements
init: install env

lint: ## Run black, ruff, mypy and pylint
lint:
	black src
	ruff src
	mypy src
	pylint src
