SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run mypy local_ip_bookkeeper tests/**/*.py
	poetry run flake8 ./local_ip_bookkeeper

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: test
test: lint package unit

