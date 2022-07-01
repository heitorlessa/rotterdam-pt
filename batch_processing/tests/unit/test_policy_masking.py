import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext
from pytest_mock import MockerFixture

from src.policy_masking import app


@pytest.fixture(autouse=True)
def disable_idempotency_network_call(monkeypatch):
    # More info at https://awslabs.github.io/aws-lambda-powertools-python/latest/utilities/idempotency/#disabling-the-idempotency-utility
    monkeypatch.setenv("POWERTOOLS_IDEMPOTENCY_DISABLED", 1)


def test_policy_masking_lambda_handler(
    policy_requests_event: dict, lambda_context: LambdaContext, mocker: MockerFixture
):
    ret = app.lambda_handler(policy_requests_event, lambda_context)
    assert ret == {"batchItemFailures": []}
