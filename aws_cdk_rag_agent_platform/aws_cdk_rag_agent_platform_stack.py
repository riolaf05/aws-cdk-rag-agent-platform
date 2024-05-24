# Example automatically generated from non-compiling source. May contain errors.
from bedrock_agent import OpenSearchServerlessStorageConfiguration, OpenSearchServerlessConfiguration, OpenSearchFieldMapping, DataSource, DataSourceConfiguration, S3Configuration, OpenSearchServerlessStorageConfiguration, PineconeConfiguration, PineconeFieldMapping, DataSource, DataSourceConfiguration, S3Configuration
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda,
    aws_s3_deployment as s3_deployment,
    aws_opensearchserverless as aws_opss,
    aws_bedrock as bedrock #L1,
)
# from cdklabs.generative_ai_cdk_constructs import ( #L2 does not works
#     bedrock
# )

#L3 https://constructs.dev/packages/bedrock-agents-cdk/v/0.0.11?lang=python#example--create-an-agent-with-2-action-groups-and-2-knowledge-bases-that-you-associate-with-the-agent
from bedrock_agent import OpenSearchServerlessStorageConfiguration, OpenSearchServerlessConfiguration, OpenSearchFieldMapping, DataSource, DataSourceConfiguration, S3Configuration, OpenSearchServerlessStorageConfiguration, PineconeConfiguration, PineconeFieldMapping, DataSource, DataSourceConfiguration, S3Configuration 
from bedrock_agent import BedrockAgent, BedrockKnowledgeBase
from constructs import Construct
import json

app = cdk.App()
stack = cdk.Stack(app, "BedrockKnowledgeBaseStack")

bucket_name = "RioRAGTestBucket"
lambda_name = "RioAgentTestLambda"
openai_spec_key="openai_spec.yaml"
agent_name = "MyTestAgent"
open_search_collection_name = "my-os-collection"
open_search_kb_name = "MyTestOpenSearchKnowledgeBase"
action_group_name1 = "MyTestActionGroup1"
foundation_model = "anthropic.claude-instant-v1"
agent_instruction = "This is a template instruction for my agent. You were created by AWS CDK."
kb_instruction = "This is a template instruction for my knowledge base. You were created by AWS CDK."
vector_index_name = "my-test-index"
vector_field_name = "my-test-vector"
text_field = "text-field"
metadata_field = "metadata-field"
open_search_storage_configuration_type = "OPENSEARCH_SERVERLESS"

class AwsCdkRagAgentPlatformStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 Bucket for RAG data
        bucket = s3.Bucket(self, bucket_name,
            versioned=False,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True)
        
        # S3 bucket for openAPI specification
        openaispec_bucket = s3.Bucket(self, bucket_name+"OpenAISpec",
                    versioned=False,
                    removal_policy=cdk.RemovalPolicy.DESTROY,
                    auto_delete_objects=True
                    )
        # Upload openAPI specification to the bucket
        s3_deployment.BucketDeployment(self, bucket_name+"OpenAISpecFile",
            sources=[s3_deployment.Source.asset("specs/")],
            destination_bucket=openaispec_bucket,
            destination_key_prefix=""
        )
            
        # Lambda for agent execution 
        agent_lambda = aws_lambda.Function(
            self, lambda_name,
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.from_asset("aws_cdk_rag_agent_platform/src"),
            handler='lambda-handler.handler',
        )

        # Bedrock Agent IAM role
        agent_resource_role_arn = iam.Role(self, "BedrockAgentRole",
            role_name="AmazonBedrockExecutionRoleForAgents_agent_test",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")]
        ).role_arn

        # Bedrock Knowledge Base IAM role
        knowledge_base_role_arn = iam.Role(self, "BedrockKnowledgeBaseRole",
            role_name="AmazonBedrockExecutionRoleForKnowledgeBase_kb_test",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")]
        ).role_arn

        # # Opensearch collection for RAG data
        #FIXME 
        # user_name = self.node.try_get_context('user_name')
        # ops_iam_user = iam.User.from_user_name(self, "OpsAdminUser", user_name)
        # network_security_policy = json.dumps([{
        #     "Rules": [
        #         {
        #         "Resource": [
        #             f"collection/{open_search_collection_name}"
        #         ],
        #         "ResourceType": "dashboard"
        #         },
        #         {
        #         "Resource": [
        #             f"collection/{open_search_collection_name}"
        #         ],
        #         "ResourceType": "collection"
        #         }
        #     ],
        #     "AllowFromPublic": True
        #     }], indent=2)

        # cfn_network_security_policy = aws_opss.CfnSecurityPolicy(self, "NetworkSecurityPolicy",
        # policy=network_security_policy,
        # name=f"{open_search_collection_name}-security-policy",
        # type="network"
        # )

        # encryption_security_policy = json.dumps({
        # "Rules": [
        #     {
        #     "Resource": [
        #         f"collection/{open_search_collection_name}"
        #     ],
        #     "ResourceType": "collection"
        #     }
        # ],
        # "AWSOwnedKey": True
        # }, indent=2)

        # cfn_encryption_security_policy = aws_opss.CfnSecurityPolicy(self, "EncryptionSecurityPolicy",
        # policy=encryption_security_policy,
        # name=f"{open_search_collection_name}-security-policy",
        # type="encryption"
        # )

        # cfn_collection = aws_opss.CfnCollection(self, "OpssSearchCollection",
        #     name=open_search_collection_name,
        #     description="Collection to be used for search using OpenSearch Serverless",
        #     type="VECTORSEARCH" # [SEARCH, TIMESERIES, VECTORSEARCH]
        # )
        # cfn_collection.add_dependency(cfn_network_security_policy)
        # cfn_collection.add_dependency(cfn_encryption_security_policy)

        # data_access_policy = json.dumps([
        # {
        #     "Rules": [
        #     {
        #         "Resource": [
        #         f"collection/{open_search_collection_name}"
        #         ],
        #         "Permission": [
        #         "aoss:CreateCollectionItems",
        #         "aoss:DeleteCollectionItems",
        #         "aoss:UpdateCollectionItems",
        #         "aoss:DescribeCollectionItems"
        #         ],
        #         "ResourceType": "collection"
        #     },
        #     {
        #         "Resource": [
        #         f"index/{open_search_collection_name}/*"
        #         ],
        #         "Permission": [
        #         "aoss:CreateIndex",
        #         "aoss:DeleteIndex",
        #         "aoss:UpdateIndex",
        #         "aoss:DescribeIndex",
        #         "aoss:ReadDocument",
        #         "aoss:WriteDocument"
        #         ],
        #         "ResourceType": "index"
        #     }
        #     ],
        #     "Principal": [
        #         ops_iam_user.user_arn,
        #         agent_resource_role_arn,
        #         knowledge_base_role_arn
        #     ],
        #     "Description": "data-access-rule"
        # }
        # ], indent=2)

        # # Knowledge Base
        # my_open_search_kb = BedrockKnowledgeBase(self, "BedrockOpenSearchKnowledgeBase",
        #     name=open_search_kb_name,
        #     role_arn=knowledge_base_role_arn,
        #     storage_configuration=OpenSearchServerlessStorageConfiguration(
        #         opensearch_serverless_configuration=OpenSearchServerlessConfiguration(
        #             collection_arn=cfn_collection.attr_arn,
        #             field_mapping=OpenSearchFieldMapping(
        #                 metadata_field=metadata_field,
        #                 text_field=text_field,
        #                 vector_field=vector_field_name
        #             ),
        #             vector_index_name=vector_index_name
        #         ),
        #         type=open_search_storage_configuration_type
        #     ),
        #     data_source=DataSource(
        #         data_source_configuration=DataSourceConfiguration(
        #             s3_configuration=S3Configuration(
        #                 bucket_arn=bucket.bucket_arn
        #             )
        #         )
        #     )
        # )

        # # Agent
        # agent = BedrockAgent(self, "BedrockAgent",
        #     agent_name=agent_name,
        #     instruction=agent_instruction,
        #     foundation_model=foundation_model,
        #     agent_resource_role_arn=agent_resource_role_arn,
        #     action_groups=[{
        #         "actionGroupName": action_group_name1,
        #         "actionGroupExecutor": agent_lambda.function_arn,
        #         # "idleSessionTTLInSeconds": 60,
        #         "agentVersion": 'DRAFT',
        #         "s3BucketName": bucket_name+"OpenAISpec",
        #         "s3ObjectKey": openai_spec_key,
        #         "desription": "This is a test action group 1 description."
        #         }
        #     ],
        #     knowledge_base_associations=[{
        #         "knowledgeBaseName": open_search_kb_name,
        #         "instruction": kb_instruction
        #         }
        #     ]
        # )

        # agent.node.add_dependency(my_open_search_kb)
        