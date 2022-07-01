import json
from typing import Optional
from uuid import uuid4


def build_apigw_event(method: str, path: str, data: Optional[dict] = None) -> dict:
    event = {
        "path": path,
        "httpMethod": method,
        "requestContext": {"requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef"},
    }

    if data is not None:
        event["body"] = json.dumps(data)

    return event


def build_fake_collect_payment_request() -> dict:
    return {
        "capture_request": f"fake-{uuid4}",
        "customer_id": f"fake-{uuid4}",
    }
