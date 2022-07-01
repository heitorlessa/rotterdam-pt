import json

import boto3
from mypy_boto3_sqs import SQSClient

from tests import utils


def test_ingest_policy(policy_queue):
    policies = [utils.build_fake_policy_requests() for _ in range(200)]
    sqs: SQSClient = boto3.client("sqs")
    for policy in policies:
        sqs.send_message(QueueUrl=policy_queue, MessageBody=json.dumps(policy))
