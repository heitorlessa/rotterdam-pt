import os

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.batch import BatchProcessor, EventType, batch_processor
from aws_lambda_powertools.utilities.idempotency import DynamoDBPersistenceLayer, IdempotencyConfig, idempotent_function
from aws_lambda_powertools.utilities.typing import LambdaContext

from .models import PolicySqs

TABLE = os.getenv("IDEMPOTENCY_TABLE", "")


processor = BatchProcessor(event_type=EventType.SQS, model=PolicySqs)
tracer = Tracer()
logger = Logger()

dynamodb = DynamoDBPersistenceLayer(table_name=TABLE)
config = IdempotencyConfig(
    event_key_jmespath="body.Policy.i_promise_is_idempotent",
    use_local_cache=True,
)


@tracer.capture_method
@idempotent_function(data_keyword_argument="record", config=config, persistence_store=dynamodb)
def record_handler(record: PolicySqs):
    logger.info({"our_field": record.body.Policy.i_promise_is_idempotent})
    logger.info(record.body.json())


@logger.inject_lambda_context
@tracer.capture_lambda_handler
@batch_processor(record_handler=record_handler, processor=processor)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """Lambda function entrypoint

    Parameters
    ----------
    event : dict
        SQS Lambda Event
    context : LambdaContext
        Lambda Context

    Returns
    -------
    dict
        SQS Batch Item Failures
    """
    return processor.response()
