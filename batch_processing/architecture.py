# diagram.py
from diagrams import Cluster, Diagram
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.integration import SimpleNotificationServiceSnsTopic, SimpleQueueServiceSqsQueue

with Diagram("architecture", show=True):
    policy_topic = SimpleNotificationServiceSnsTopic("Policy Topic")
    with Cluster("Policy Requests Batching"):
        policy_queue = SimpleQueueServiceSqsQueue("Aggregation queue")
        with Cluster("Policy masking"):
            policy_masking_fn = LambdaFunction("Policy function")

    policy_topic >> policy_queue >> policy_masking_fn
