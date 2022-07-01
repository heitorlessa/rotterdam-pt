from __future__ import annotations

import json
from typing import Any, Optional

from aws_lambda_powertools.utilities.parser import validator
from aws_lambda_powertools.utilities.parser.models.sqs import SqsRecordModel
from pydantic import BaseModel


def scrub_data(value: str):
    return "###########"


class Policyholder(BaseModel):
    date_of_birth: str
    email_address: str
    licence_pass_date: Any
    phone_number: str
    mobile_number: str
    full_name: str
    forenames: str
    surname: str
    house_name_or_number: str
    address_line_1: str
    address_line_2: str
    address_line_3: str
    postcode: str

    _scrub_all = validator("*", allow_reuse=True)(scrub_data)


class Policy(BaseModel):
    event_date: str
    event_effective_date: str
    insurance_company: str
    oldest_driver_dob: str
    youngest_driver_dob: str
    policyholder: Policyholder
    policy_number: str
    renewal_date: str
    starting_score: int
    status: str
    transaction_type: str
    cover_start_date: str
    end_date: str
    i_promise_is_idempotent: Optional[str]

    # validators
    _scrub_oldest = validator("oldest_driver_dob", allow_reuse=True)(scrub_data)
    _scrub_youngest = validator("youngest_driver_dob", allow_reuse=True)(scrub_data)


class PolicyModel(BaseModel):
    Policy: Policy


class PolicySqs(SqsRecordModel):

    body: PolicyModel
    # auto transform json string
    # so Pydantic can auto-initialize nested Order model
    @validator("body", pre=True)
    def transform_body_to_dict(cls, value: str):
        return json.loads(value)
