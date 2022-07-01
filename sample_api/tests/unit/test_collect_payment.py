from aws_lambda_powertools.utilities.typing import LambdaContext

from src.payment import app


def test_collect_payment_lambda_handler(lambda_context: LambdaContext, collect_payment_event: dict):
    ret = app.lambda_handler(collect_payment_event, lambda_context)
    assert ret["statusCode"] == 200
