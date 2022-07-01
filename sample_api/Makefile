
.PHONY: target dev format lint test coverage-html pr docs
.PHONY: security-baseline complexity-baseline

STACK_NAME ?= "rotterdam-pt-api"
FUNCTION ?= "CollectPaymentFunction"

target:
	@$(MAKE) pr

dev:
	pip install --upgrade pip pre-commit poetry cfn-lint aws-sam-cli
# NOTE: You can use pipx to isolate Python-based CLIs too
# pipx install poetry cfn-lint aws-sam-cli
	poetry install
	pre-commit install

docs:
	poetry run mkdocs serve

format:
	poetry run isort src tests
	poetry run black src tests

lint: format static-checker
	poetry run flake8 src/* tests/*

lint-infra:
	cfn-lint template.yaml

test:
	poetry run pytest

unit-test:
	poetry run pytest tests/unit -s

integ-test:
	poetry run pytest tests/integ

e2e-test:
	poetry run pytest tests/e2e

coverage-html:
	poetry run pytest --cov=src --cov-report=html

pre-commit:
	pre-commit run --show-diff-on-failure

pr: lint-infra lint pre-commit static-checker test security-baseline complexity-baseline

security-baseline:
	poetry run bandit -r src

complexity-baseline:
	$(info Maintenability index)
	poetry run radon mi src
	$(info Cyclomatic complexity index)
	poetry run xenon --max-absolute C --max-modules A --max-average A src

static-checker:
	poetry run mypy --pretty src

logs:
	sam logs -n ${FUNCTION} --stack-name ${STACK_NAME} -t

traces:
	sam traces

watch: build-layers
	sam sync --stack-name ${STACK_NAME} --watch --no-dependency-layer

deploy: build-layers
	sam deploy

build-layers:
# NOTE: Encryption and Pydantic use C-bindings thus requiring a Linux target build
	poetry export --format requirements.txt > lambda_layers/requirements.txt
	sam build --cached --use-container

sam-to-cloudformation:
# NOTE: Use this when you need to troubleshoot CloudFormation equivalence, or OpenAPI spec
	sam validate 2> debug.yaml --debug
