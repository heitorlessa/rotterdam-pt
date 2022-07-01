import json
import os
from dataclasses import dataclass

import pytest
from aws_lambda_powertools.utilities.parameters import get_parameter

from tests import utils


@pytest.fixture
def lambda_context():
    @dataclass(repr=False, order=False)
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = "arn:aws:lambda:eu-west-1:809313241:function:test"
        aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

    return LambdaContext()


@pytest.fixture
def stack_config():
    stage = os.getenv("STAGE")
    cfg = get_parameter(name=f"/{stage}/service/sample_payment/test/config")
    return json.loads(cfg)


@pytest.fixture
def collect_payment_function(stack_config: dict):
    return stack_config["CollectPaymentFunction"]


@pytest.fixture
def payment_api(stack_config: dict):
    return stack_config["PaymentApiEndpoint"]


@pytest.fixture
def stage(stack_config: dict):
    return stack_config["Stage"]


@pytest.fixture
def hello_event() -> dict:
    return utils.build_apigw_event(method="GET", path="/hello")


@pytest.fixture
def collect_payment_event(collect_payment_request: dict) -> dict:
    return utils.build_apigw_event(method="POST", path="/collect", data=collect_payment_request)


@pytest.fixture
def collect_payment_request():
    with open("./tests/data/collect_payment_request.json") as fp:
        return json.load(fp)
