import json
from uuid import uuid4

from faker import Faker

faker = Faker()


def build_sqs_event(data: dict, records: int = 1) -> dict:
    """Build dummy SQS event

    Parameters
    ----------
    records : int
        number of records to generate

    Returns
    -------
    dict
        SQS event
    """

    return {
        "Records": [
            {
                "messageId": f"{uuid4()}",
                "receiptHandle": "MessageReceiptHandle",
                "body": json.dumps(data),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
                "messageAttributes": {},
                "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:eu-west-1:123456789012:MyQueue",
                "awsRegion": "eu-west-1",
            }
            for _ in range(records)
        ]
    }


def build_fake_policy_requests() -> dict:
    full_name = faker.name()
    dob = faker.date_of_birth().isoformat()

    return {
        "Policy": {
            "i_promise_is_idempotent": "we were right",
            "event_date": faker.date_this_month().isoformat(),
            "event_effective_date": faker.date_this_month().isoformat(),
            "insurance_company": "TK/SO",
            "oldest_driver_dob": dob,
            "youngest_driver_dob": f"{faker.date_of_birth().isoformat()}",
            "policyholder": {
                "date_of_birth": dob,
                "email_address": faker.email(),
                "licence_pass_date": "",
                "phone_number": faker.phone_number(),
                "mobile_number": faker.phone_number(),
                "full_name": full_name,
                "forenames": full_name.split()[0],
                "surname": full_name.split()[1],
                "house_name_or_number": faker.building_number(),
                "address_line_1": f"{faker.street_suffix()} {faker.street_name()}",
                "address_line_2": "Somewhere",
                "address_line_3": "",
                "postcode": faker.postcode(),
            },
            "policy_number": "test",
            "renewal_date": "2022-12-10T00:00:00+01:00",
            "starting_score": 50,
            "status": "Confirmed",
            "transaction_type": "NewBusiness",
            "cover_start_date": "2022-01-01T16:40:10.918+00:00",
            "end_date": "2022-12-31T16:40:10.919+00:00",
        }
    }
