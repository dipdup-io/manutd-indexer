.ONESHELL:
.DEFAULT_GOAL: all

py := poetry run

source_dir := .
unit_tests_dir := tests

dipdup_args := -e .env -c .

test:
	PYTHONPATH=. $(py) pytest tests/

install:
	poetry install `if [ "${DEV}" = "0" ]; then echo "--only main"; fi` --sync

isort:
	$(py) isort $(source_dir) $(unit_tests_dir)

ssort:
	$(py) ssort $(source_dir) $(unit_tests_dir)

black:
	$(py) black $(source_dir) $(unit_tests_dir)

ruff:
	$(py) ruff check --fix-only --show-fixes $(source_dir) $(unit_tests_dir)

mypy:
	$(py) mypy $(source_dir) $(unit_tests_dir)

lint: isort ssort black ruff mypy

wipe:
	$(py) dipdup $(dipdup_args) schema wipe --force

init:
	$(py) dipdup $(dipdup_args) init

run:
	$(py) dipdup $(dipdup_args) run

up:
	docker-compose up -d --build --remove-orphans --force-recreate

down:
	docker-compose down --volumes
