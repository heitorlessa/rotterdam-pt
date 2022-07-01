# diagram.py
from diagrams import Diagram
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.network import APIGateway
from diagrams.generic.place import Datacenter

with Diagram("architecture", show=True):
    payment_api = APIGateway("Payment API")
    collect_payment_fn = LambdaFunction("Payment collection")
    payment_provider = Datacenter("Payment provider")

    payment_api >> collect_payment_fn >> payment_provider
