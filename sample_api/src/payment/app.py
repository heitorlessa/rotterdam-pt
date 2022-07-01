from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

logger = Logger()
tracer = Tracer()
app = APIGatewayRestResolver()


@app.get("/hello")
def hello_world():
    app.current_event.get
    return {"message": "hello universe"}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event, context) -> dict:
    return app.resolve(event, context)
