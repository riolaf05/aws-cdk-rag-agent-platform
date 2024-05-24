import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_rag_agent_platform.aws_cdk_rag_agent_platform_stack import AwsCdkRagAgentPlatformStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cdk_rag_agent_platform/aws_cdk_rag_agent_platform_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCdkRagAgentPlatformStack(app, "aws-cdk-rag-agent-platform")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
